# row path one - /html/body/fact-check-tools/div/mat-sidenav-container/mat-sidenav-content/search-results-page/div/div[6]/fc-results-list/div[1]/div/div[3]/div[3]/div/span/span[1]
# row path two - /html/body/fact-check-tools/div/mat-sidenav-container/mat-sidenav-content/search-results-page/div/div[6]/fc-results-list/div[2]/div/div[3]/div[2]/div/span/span[1]
# row i fact check 1 - /html/body/fact-check-tools/div/mat-sidenav-container/mat-sidenav-content/search-results-page/div/div[6]/fc-results-list/div[41]/div/div[3]/div[2]/div[1]/span/span[1]
# row i fact check 2 - /html/body/fact-check-tools/div/mat-sidenav-container/mat-sidenav-content/search-results-page/div/div[6]/fc-results-list/div[41]/div/div[3]/div[2]/div[2]/span/span[1]

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in PATH or provide the full path
driver.get("https://toolbox.google.com/factcheck/explorer/search/list:recent;hl=")

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//fc-results-list")))

# Initialize data storage
fact_check_data = []

try:
    i = 1  # Start with the first row
    while True:  # Infinite loop to iterate rows
        # Define the row XPath
        row_xpath = f"/html/body/fact-check-tools/div/mat-sidenav-container/mat-sidenav-content/search-results-page/div/div[6]/fc-results-list/div[{i}]"
        time.sleep(2)  # Allow time for the row to load

        # Check if the row exists
        if not driver.find_elements(By.XPATH, row_xpath):
            break  # Exit loop if row does not exist

        # Check for single or multiple fact-check sources
        multiple_sources_xpath = f"{row_xpath}/div/div[3]/div[2]/div"
        single_source_xpath = f"{row_xpath}/div/div[3]/div[3]/div/span/span[1]"

        # Handle multiple fact-check sources
        if driver.find_elements(By.XPATH, multiple_sources_xpath):
            j = 1  # Start with the first fact check
            while True:
                fact_check_xpath = f"{row_xpath}/div/div[3]/div[2]/div[{j}]/span/span[1]"
                if not driver.find_elements(By.XPATH, fact_check_xpath):
                    break  # Exit loop if no more fact-check sources exist

                # Extract text
                fact_check_text = driver.find_element(By.XPATH, fact_check_xpath).text
                print(f"Row {i}, Fact Check {j}: {fact_check_text}")

                # Store the data
                fact_check_data.append({
                    "Row": i,
                    "Fact Check Number": j,
                    "Fact Check Text": fact_check_text
                })

                j += 1  # Move to the next fact check

        # Handle single fact-check source
        elif driver.find_elements(By.XPATH, single_source_xpath):
            fact_check_text = driver.find_element(By.XPATH, single_source_xpath).text
            print(f"Row {i}, Single Fact Check: {fact_check_text}")

            # Store the data
            fact_check_data.append({
                "Row": i,
                "Fact Check Number": 1,
                "Fact Check Text": fact_check_text
            })

        else:
            print(f"No fact checks found for row {i}.")

        # Move to the next row
        print(f"Processed row {i}")
        i += 1
        time.sleep(5)  # Additional delay to ensure the next row is loaded

finally:
    # Close the browser
    driver.quit()

# Save data to a CSV
df = pd.DataFrame(fact_check_data)
df.to_csv("recent_google.csv", index=False)
print("Data saved to 'recent_google_final.csv'")

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import pandas as pd
# import time

# # Set up Selenium WebDriver
# driver = webdriver.Chrome()  # Ensure chromedriver is in PATH or provide the full path
# driver.get("https://toolbox.google.com/factcheck/explorer/search/list:recent;hl=")

# # Initialize data storage
# fact_check_data = []

# try:
#     time.sleep(10)  # Wait for the initial page to load
#     previous_row_count = 0  # Keep track of previously loaded rows
#     max_retries = 5  # Limit retries to prevent infinite scrolling
#     retries = 0

#     while retries < max_retries:
#         # Get the current rows
#         rows = driver.find_elements(By.XPATH, "//fc-results-list/div")
#         current_row_count = len(rows)
#         print(f"Found {current_row_count} rows.")

#         # Check if new rows have loaded
#         if current_row_count > previous_row_count:
#             retries = 0  # Reset retries if new rows are loaded
#             previous_row_count = current_row_count

#             # Process all rows
#             for i in range(1, current_row_count + 1):
#                 row_xpath = f"/html/body/fact-check-tools/div/mat-sidenav-container/mat-sidenav-content/search-results-page/div/div[4]/fc-results-list/div[{i}]"
#                 print(f"Processing row {i}...")

#                 try:
#                     # Check for multiple sources
#                     multiple_sources_xpath = f"{row_xpath}/div/div[3]/div[2]/div"
#                     single_source_xpath = f"{row_xpath}/div/div[3]/div[3]/div/span/span[1]"

#                     # Handle multiple fact-check sources
#                     if driver.find_elements(By.XPATH, multiple_sources_xpath):
#                         j = 1
#                         while True:
#                             fact_check_xpath = f"{row_xpath}/div/div[3]/div[2]/div[{j}]/span/span[1]"
#                             if not driver.find_elements(By.XPATH, fact_check_xpath):
#                                 break  # Exit loop if no more fact-check sources exist

#                             fact_check_text = driver.find_element(By.XPATH, fact_check_xpath).text.strip()
#                             if fact_check_text:
#                                 print(f"Row {i}, Fact Check {j}: {fact_check_text}")
#                                 fact_check_data.append({
#                                     "Row": i,
#                                     "Fact Check Number": j,
#                                     "Fact Check Text": fact_check_text
#                                 })
#                             else:
#                                 print(f"Row {i}, Fact Check {j}: No text found.")
#                             j += 1

#                     # Handle single fact-check source
#                     elif driver.find_elements(By.XPATH, single_source_xpath):
#                         fact_check_text = driver.find_element(By.XPATH, single_source_xpath).text.strip()
#                         if fact_check_text:
#                             print(f"Row {i}, Single Fact Check: {fact_check_text}")
#                             fact_check_data.append({
#                                 "Row": i,
#                                 "Fact Check Number": 1,
#                                 "Fact Check Text": fact_check_text
#                             })
#                         else:
#                             print(f"Row {i}, Single Fact Check: No text found.")

#                 except Exception as e:
#                     print(f"Error processing row {i}: {e}")

#             # Scroll to load more rows
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(5)  # Wait for new rows to load

#         else:
#             # No new rows loaded, increment retry counter
#             retries += 1
#             print(f"No new rows found. Retry {retries} of {max_retries}.")
#             time.sleep(2)

# finally:
#     # Close the browser
#     driver.quit()

# # Save data to a CSV
# if fact_check_data:
#     df = pd.DataFrame(fact_check_data)
#     df.to_csv("google_recents.csv", index=False)
#     print("Data saved to 'google_recents.csv'")
# else:
#     print("No data extracted.")
