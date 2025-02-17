import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# List of websites to scrape
websites = [
    "https://pesacheck.org/tagged/burkina-faso",
    "https://pesacheck.org/tagged/burundi",
    "https://pesacheck.org/tagged/cameroon",
    'https://stopintox.cm/',
    'https://factuel.afp.com/AFP-Cote-dIvoire',
    'https://pesacheck.org/',
    'https://congocheck.net/home/',
    'https://akhbarmeter.org/',
    'https://www.saheeh.news/',
    'https://tafnied.com/'
]

# Function to scrape all URLs from the main page
def scrape_all_links(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all links
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(url, href)  # Resolve relative URLs to absolute
            links.append(full_url)

        return list(set(links))  # Deduplicate links
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Main scraping function
def scrape_websites(websites):
    results = []
    for site in websites:
        print(f"Scraping: {site}")
        links = scrape_all_links(site)
        results.extend([{"Website": site, "URL": link} for link in links])
    return results

# Scrape websites
all_links = scrape_websites(websites)

# Save results to CSV
df = pd.DataFrame(all_links)
df.to_csv("all_links_main_pages.csv", index=False)
print("All links saved to 'all_links_main_pages.csv'")
