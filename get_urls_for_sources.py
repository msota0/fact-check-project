from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Load the Excel file
file_name = "news_fact_checker_websites.xlsx"
df = pd.read_excel(file_name)

# Ensure the 'content' field contains the names of the websites
fact_check_websites = df['content'].tolist()

# Set up Selenium WebDriver
# driver_path = "path/to/your/chromedriver"  # Replace with your ChromeDriver path
driver = webdriver.Chrome()

# Function to search and scrape URLs using Yahoo
def search_url_yahoo(query):
    try:
        # Navigate to Yahoo
        driver.get("https://search.yahoo.com/")
        search_box = driver.find_element(By.NAME, "p")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load
        time.sleep(2)
        
        # Extract the first result URL
        results = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div/div[1]/div/div/div/div/ol/li[1]/div/div[1]/h3/a")
        if results:
            return results[0].get_attribute("href")
    except Exception as e:
        print(f"Error for query '{query}': {e}")
    return None

# Create a list to store URLs
urls = []

# Iterate through website names and fetch URLs
for site in fact_check_websites:
    url = search_url_yahoo(site)
    urls.append(url)
    print(f"Processed: {site} -> {url}")

# Close the browser
driver.quit()

# Add the URLs to the DataFrame
df['URL'] = urls

# Save the updated DataFrame back to Excel
output_file = "news_fact_checker_websites_with_urls.xlsx"
df.to_excel(output_file, index=False)
print(f"Updated file saved as {output_file}")
