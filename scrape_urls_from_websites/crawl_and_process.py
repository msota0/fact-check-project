# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# from googletrans import Translator
# import pandas as pd
# import time

# # Initialize Google Translate
# translator = Translator()

# # Track visited links to avoid revisiting
# visited_links = set()

# # Set maximum depth and maximum number of links to crawl
# MAX_DEPTH = 2
# MAX_LINKS = 500

# # Function to fetch page content
# def fetch_content(url):
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         return response.text
#     except Exception as e:
#         print(f"Error fetching {url}: {e}")
#         return None

# # Function to check if the content is an article
# def is_article(content, url):
#     try:
#         soup = BeautifulSoup(content, "html.parser")
        
#         # Check for article-like metadata
#         title = soup.title.string if soup.title else ""
#         meta_og_type = soup.find("meta", property="og:type")
#         meta_og_title = soup.find("meta", property="og:title")

#         # Extract text from <p> tags
#         body_text = " ".join([p.get_text() for p in soup.find_all("p")]).strip()
        
#         # Skip if body_text is empty
#         if not body_text:
#             print(f"Skipped validation for {url}: No body text found.")
#             return False

#         # Detect and translate language
#         lang = translator.detect(body_text[:500]).lang  # Detect language of the first 500 characters
#         if lang != "en":
#             body_text = translator.translate(body_text, src=lang, dest="en").text

#         # Validate based on text length and metadata
#         if len(body_text.split()) > 100 or "article" in title.lower() or (meta_og_type and "article" in meta_og_type["content"].lower()):
#             return True
#     except Exception as e:
#         print(f"Error validating article for {url}: {e}")
#     return False

# # Function to scrape all links on a page
# def scrape_links(url, depth=0):
#     if depth > MAX_DEPTH or len(visited_links) >= MAX_LINKS:
#         return []  # Stop crawling if maximum depth or link limit is reached
    
#     try:
#         content = fetch_content(url)
#         if not content:
#             return []
        
#         soup = BeautifulSoup(content, "html.parser")
#         links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
#         return list(set(links))  # Deduplicate links
#     except Exception as e:
#         print(f"Error scraping links from {url}: {e}")
#         return []

# # Main function to process URLs
# def process_urls(input_file, output_file):
#     df = pd.read_csv(input_file)
#     validated_urls = []

#     for index, row in df.iterrows():
#         url = row["URL"]
#         if url in visited_links:
#             continue  # Skip already visited links
        
#         visited_links.add(url)
#         print(f"Processing: {url}")
        
#         # Fetch content and validate
#         content = fetch_content(url)
#         if content and is_article(content, url):
#             print(f"Valid article: {url}")
#             validated_urls.append({"URL": url, "Status": "Article"})
        
#         # Crawl further links on valid pages
#         new_links = scrape_links(url, depth=1)
#         for new_url in new_links:
#             if new_url not in visited_links:
#                 visited_links.add(new_url)
#                 validated_urls.append({"URL": new_url, "Status": "To Be Validated"})
        
#         # Sleep to avoid hitting rate limits
#         time.sleep(2)

#     # Save validated URLs
#     pd.DataFrame(validated_urls).to_csv(output_file, index=False)
#     print(f"Validated URLs saved to {output_file}")

# # Run the crawler
# process_urls("all_links_main_pages.csv", "final_validated_articles.csv")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from googletrans import Translator
import pandas as pd
import time
from collections import deque

# Initialize Google Translate
translator = Translator()

visited_links = set()

# Set maximum depth and maximum number of links to crawl
MAX_DEPTH = 2
MAX_LINKS = 500

# Websites to start crawling from
# websites = [
#     "https://pesacheck.org/tagged/burkina-faso",
#     "https://pesacheck.org/tagged/burundi",
#     "https://pesacheck.org/tagged/cameroon",
#     'https://stopintox.cm/',
#     'https://factuel.afp.com/AFP-Cote-dIvoire',
#     'https://pesacheck.org/',
#     'https://congocheck.net/home/',
#     'https://akhbarmeter.org/',
#     'https://www.saheeh.news/',
#     'https://tafnied.com/'
# ]

websites =  [
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

def fetch_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def is_article(content, url):
    try:
        soup = BeautifulSoup(content, "html.parser")
        
        # Check for article-like metadata
        title = soup.title.string if soup.title else ""
        meta_og_type = soup.find("meta", property="og:type")
        meta_og_title = soup.find("meta", property="og:title")

        body_text = " ".join([p.get_text() for p in soup.find_all("p")]).strip()
        
        if not body_text or len(body_text.split()) < 50:  # Reduced threshold for homepages with many articles
            print(f"Skipped {url}: No significant body text found.")
            return False

        lang = translator.detect(body_text[:500]).lang  # Detect language of the first 500 characters
        if lang != "en":
            body_text = translator.translate(body_text, src=lang, dest="en").text

        # Validate based on text length and metadata
        if "article" in title.lower() or (meta_og_type and "article" in meta_og_type["content"].lower()):
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
            print(f"Skipping social media link: {link}")
            continue

        # Ignore non-article links based on EXCLUDE_KEYWORDS
        if any(keyword in parsed_link.path.lower() for keyword in EXCLUDE_KEYWORDS):
            print(f"Skipping navigation link: {link}")
            continue

        # Prioritize links that contain ARTICLE_KEYWORDS
        if any(keyword in parsed_link.path.lower() for keyword in ARTICLE_KEYWORDS) or len(parsed_link.path.split("/")) > 2:
            valid_links.append(link)

    return list(set(valid_links))  

def scrape_links(url):
    try:
        content = fetch_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, "html.parser")
        raw_links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
        return filter_links(raw_links, url)
    except Exception as e:
        print(f"Error scraping links from {url}: {e}")
        return []

def crawl_websites(start_urls, output_file):
    queue = deque(start_urls)
    validated_urls = []
    
    while queue and len(visited_links) < MAX_LINKS:
        url = queue.popleft()
        base_website = urlparse(url).netloc  
        if url in visited_links:
            continue 
        
        visited_links.add(url)
        print(f"Processing: {url}")
        
        content = fetch_content(url)
        if content and is_article(content, url):
            print(f"Valid article: {url}")
            validated_urls.append({"Website": base_website, "URL": url, "Status": "Article"})
        else:
            print(f"Not an article: {url}")
        
        new_links = scrape_links(url)
        for new_url in new_links:
            if new_url not in visited_links:
                queue.append(new_url)
                validated_urls.append({"Website": base_website, "URL": new_url, "Status": "To Be Validated"})
        
        time.sleep(2)
    
    pd.DataFrame(validated_urls).to_csv(output_file, index=False)
    print(f"Validated URLs saved to {output_file}")

scrawl_websites(websites, "article_links.csv")


