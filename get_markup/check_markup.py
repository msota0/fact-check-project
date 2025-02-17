import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the cleaned data
input_file = "news_fact_checker_websites.xlsx"
df = pd.read_excel(input_file)

# Initialize results
results = []

# Iterate through each website
for index, row in df.iterrows():
    website = row['content']
    try:
        # Fetch the website content
        response = requests.get(website, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Search for JSON-LD or microdata with "Review" or "ClaimReview"
        found_markup = False
        for script in soup.find_all('script', type='application/ld+json'):
            if "Review" in script.text or "ClaimReview" in script.text:
                found_markup = True
                break

        # Append results
        results.append({
            "Website": website,
            "Clean Review Markup Present": "Yes" if found_markup else "No"
        })

    except Exception as e:
        # Handle errors (e.g., timeout, 404)
        results.append({
            "Website": website,
            "Clean Review Markup Present": "Error"
        })
        print(f"Error checking {website}: {e}")

# Save results to Excel
output_file = "fact_checker_review_markup.xlsx"
results_df = pd.DataFrame(results)
results_df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")
