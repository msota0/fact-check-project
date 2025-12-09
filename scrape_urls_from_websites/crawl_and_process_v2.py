from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from googletrans import Translator
import pandas as pd
import time
from collections import deque
from urllib.parse import urljoin, urlparse

# Initialize Google Translate
translator = Translator()

visited_links = set()

# Set maximum number of links to crawl per website
MAX_ARTICLES_PER_WEBSITE = 3
MAX_LINKS = 500

# Websites to start crawling from
websites = [
    "https://chequeado.com/",
    "https://www.altnews.in/",
    "https://www.stopfake.org/en/main/",
    "https://newschecker.in/",
    "https://www.verificat.cat/",
    "https://www.snopes.com/",
    "https://cambodia.factcrescendo.com/",
    "https://www.aosfatos.org/",
    "https://maldita.es/",
    "https://fullfact.org/",
    "https://faktograf.hr/",
    "https://nieuwscheckers.nl/",
    "https://factly.in/",
    "https://factcheckhub.com/",
    "https://boliviaverifica.bo/",
    "https://factreview.gr/",
    "https://verifica.efe.com/",
    "https://www.politifact.com/",
    "https://srilanka.factcrescendo.com/",
    "https://www.boombd.com/",
    "https://leadstories.com/",
    "https://www.factcheck.org/",
    "https://www.logicallyfacts.com/en",
    "https://www.istinomer.rs/",
    "https://www.mygopen.com/",
    "https://teyit.org/",
    "https://factcheck.afp.com/AFP-Greece",
    "https://gigafact.org/",
    "https://factcheck.bg/",
    "https://demagog.org.pl/en/",
    "https://factcheckni.org/"
]

EXCLUDE_KEYWORDS = [
    "about", "contact", "privacy", "terms", "login", "signup",
    "faq", "help", "support", "subscribe", "donate", "home", "category"
]

ARTICLE_KEYWORDS = ["fact-check", "news", "article", "2023", "2024", "post", "review"]

# Set up the WebDriver (adjust the path to ChromeDriver)
chrome_options = Options()
# driver_path = "/path/to/chromedriver"  # Update this path to your chromedriver location
service = Service()

def fetch_content(url):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(7)  # Wait for the page to load
        content = driver.page_source
        driver.quit()
        return driver  # Return the driver object, not just the content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def is_article(driver, url):
    try:
        # Check for schema markup
        if '<script type="application/ld+json" class="yoast-schema-graph">' in driver.page_source:
            print(f"Found schema markup for {url}.")
            return True

        # Find the body text and make sure it has content
        body_text = " ".join([p.text for p in driver.find_elements(By.TAG_NAME, "p")]).strip()
        if not body_text or len(body_text.split()) < 50:
            print(f"Skipped {url}: No significant body text found.")
            return False

        # Translate if necessary
        lang = translator.detect(body_text[:500]).lang
        if lang != "en":
            body_text = translator.translate(body_text, src=lang, dest="en").text

        # Check if it's an article based on title or metadata
        title = driver.title if driver.title else ""
        meta_og_type = driver.find_element(By.XPATH, "//meta[@property='og:type']")
        
        if "article" in title.lower() or (meta_og_type and "article" in meta_og_type.get_attribute("content").lower()):
            return True
    except Exception as e:
        print(f"Error validating article for {url}: {e}")
    return False

def filter_links(links, base_url):
    valid_links = []
    for link in links:
        parsed_link = urlparse(link)

        # Ignore links with social media domains
        if any(domain in parsed_link.netloc for domain in ["facebook.com", "twitter.com", "linkedin.com", "instagram.com", "youtube.com"]):
            continue

        # Ignore non-article links based on EXCLUDE_KEYWORDS
        if any(keyword in parsed_link.path.lower() for keyword in EXCLUDE_KEYWORDS):
            continue

        # Prioritize links that contain ARTICLE_KEYWORDS
        if any(keyword in parsed_link.path.lower() for keyword in ARTICLE_KEYWORDS) or len(parsed_link.path.split("/")) > 2:
            valid_links.append(link)

    return list(set(valid_links))  

def scrape_links(url):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(3)
        raw_links = [urljoin(url, a.get_attribute("href")) for a in driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
        driver.quit()

        return filter_links(raw_links, url)
    except Exception as e:
        print(f"Error scraping links from {url}: {e}")
        return []

def crawl_websites(start_urls, output_file):
    for website in start_urls:
        queue = deque([website])
        validated_urls = []
        article_count = 0
        
        while queue and len(validated_urls) < MAX_ARTICLES_PER_WEBSITE:
            url = queue.popleft()
            if url in visited_links:
                continue
            
            visited_links.add(url)
            print(f"Processing: {url}")
            
            driver = fetch_content(url)
            if driver and is_article(driver, url):
                validated_urls.append({"Website": website, "URL": url, "Status": "Article"})
                article_count += 1
                print(f"Valid article: {url}")

            # Stop after finding 3 valid articles
            if article_count >= MAX_ARTICLES_PER_WEBSITE:
                break

            new_links = scrape_links(url)
            for new_url in new_links:
                if new_url not in visited_links:
                    queue.append(new_url)
                    validated_urls.append({"Website": website, "URL": new_url, "Status": "To Be Validated"})

            time.sleep(2)

        pd.DataFrame(validated_urls).to_csv(output_file, index=False)
        print(f"Validated URLs for {website} saved to {output_file}")

crawl_websites(websites, "article_links.csv")
