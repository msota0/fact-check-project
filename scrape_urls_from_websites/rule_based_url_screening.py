import pandas as pd
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Keywords and patterns for filtering
ARTICLE_KEYWORDS = ["fact-check", "article", "news", "2023", "2024", "post"]
EXCLUDE_KEYWORDS = [
    "about", "contact", "privacy", "terms", "login", "signup", "mailto:",
    "/home", "/contact-us", "navbar", "social"
]

# Function to check if a URL is likely an article
def is_article_link(url):
    path = urlparse(url).path.lower()
    # Exclude URLs with unwanted keywords
    if any(keyword in url for keyword in EXCLUDE_KEYWORDS):
        return False
    # Include URLs with desired keywords
    if any(keyword in path for keyword in ARTICLE_KEYWORDS):
        return True
    # Check if the path has more than two words (likely an article)
    path_segments = path.strip("/").split("/")
    if len(path_segments) > 2:
        return True
    return False

# Function to validate and fetch source link from a URL
def validate_article_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Check if the page has keywords indicating a fact-check article
        if any(keyword in soup.text.lower() for keyword in ARTICLE_KEYWORDS):
            # Extract source link if available
            source_link = None
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if "source" in href.lower() or "fact-check" in href.lower():
                    source_link = urljoin(url, href)
                    break
            return {"Article URL": url, "Source Link": source_link}
    except Exception as e:
        print(f"Error validating {url}: {e}")
    return None

# Load the CSV file
input_file = "all_links_main_pages.csv"
output_file = "validated_article_links.csv"
df = pd.read_csv(input_file)

# Process each URL
validated_articles = []
for index, row in df.iterrows():
    url = row["URL"]
    if is_article_link(url):
        print(f"Processing: {url}")
        result = validate_article_url(url)
        if result:
            validated_articles.append(result)

# Save the validated articles to a new CSV file
if validated_articles:
    validated_df = pd.DataFrame(validated_articles)
    validated_df.to_csv(output_file, index=False)
    print(f"Validated article links saved to '{output_file}'.")
else:
    print("No valid articles found.")
