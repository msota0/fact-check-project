# AIzaSyCzHJnkfRR4kkNXC7oN5D_0jakrQUG6-l0
import pandas as pd
import requests
import time

def fetch_fact_check_publishers(api_key, languages, query="news", max_results=100, sleep_interval=1, max_retries=3):
    """
    Fetch all fact-checking publishers referenced by Google's Fact Check Tools API for multiple languages.
    
    Parameters:
    - api_key (str): Google Fact Check Tools API key.
    - languages (list): List of language codes to query (ISO 639-1 format).
    - query (str): Search query to find claims (default is 'news').
    - max_results (int): Maximum number of claims to fetch per language.
    - sleep_interval (int): Time in seconds to wait between consecutive API requests.
    - max_retries (int): Maximum number of retries for a failed request.
    
    Returns:
    - Set of unique publishers' website domains.
    """
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    unique_publishers = set()

    for language_code in languages:
        print(f"Fetching publishers for language: {language_code}")
        page_token = None
        retries = 0

        while True:
            params = {
                "key": api_key,
                "query": query,
                "languageCode": language_code,
                "pageSize": min(max_results, 100),
            }
            if page_token:
                params["pageToken"] = page_token

            try:
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    claims = data.get("claims", [])
                    for claim in claims:
                        for review in claim.get("claimReview", []):
                            publisher = review.get("publisher", {}).get("site", None)
                            if publisher:
                                unique_publishers.add(publisher)

                    # Check for next page token
                    page_token = data.get("nextPageToken", None)
                    if not page_token:
                        break

                elif response.status_code == 503:
                    # Retry on service unavailability
                    retries += 1
                    if retries > max_retries:
                        print(f"Max retries reached for language {language_code}. Skipping.")
                        break
                    print(f"Service unavailable for {language_code}. Retrying in {2 ** retries} seconds...")
                    time.sleep(2 ** retries)
                else:
                    print(f"Error for language {language_code}: {response.status_code}, {response.text}")
                    break

            except requests.exceptions.RequestException as e:
                retries += 1
                if retries > max_retries:
                    print(f"Max retries reached for language {language_code}. Skipping. Error: {e}")
                    break
                print(f"Network error for language {language_code}: {e}. Retrying in {2 ** retries} seconds...")
                time.sleep(2 ** retries)
                continue

            # Sleep for the specified interval to avoid hitting API rate limits
            time.sleep(sleep_interval)

    return unique_publishers

# Replace 'YOUR_API_KEY' with your actual API key
api_key = "AIzaSyCzHJnkfRR4kkNXC7oN5D_0jakrQUG6-l0"

# List of language codes (ISO 639-1)
languages = ["en", "es", "fr", "de", "zh", "hi", "ar", "ru", "pt", "ja", "ko", "it", "pl", "nl", "sv"]
# languages = ["en"]

# Fetch unique publishers from the Fact Check Tools API
unique_publishers = fetch_fact_check_publishers(api_key, languages, query="news", max_results=1000, sleep_interval=2)

# Convert the unique publishers to a DataFrame
if unique_publishers:
    publishers_df = pd.DataFrame(sorted(unique_publishers), columns=["Fact-Checking Websites"])
    # Save the DataFrame to an Excel file
    output_file = "google_fact_checker.xlsx"
    publishers_df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")
else:
    print("No publishers found.")