# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import time

# # Configure Selenium WebDriver
# options = Options()
# # options.add_argument("--headless")  # Run in headless mode
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# # service = Service('/path/to/chromedriver')  # Update with the correct path to your ChromeDriver

# # Start the WebDriver
# driver = webdriver.Chrome(options=options)

# # Target URL
# url = "https://reporterslab.org/fact-checking/#"
# driver.get(url)

# # Give the page some time to load
# time.sleep(5)  # Adjust the sleep time as needed

# # Step 1: Click the map view close button
# map_view_close_xpath = "/html/body/div[4]/div/div[2]/div[3]/div[4]/div/div/a"
# map_view_close_button = driver.find_element(By.XPATH, map_view_close_xpath)
# map_view_close_button.click()

# # Give some time for the page to update
# time.sleep(2)

# # Step 2: Click all collapsed categories/continents
# categories_xpath = "/html/body/div[3]/div[2]/div[2]/div[1]/h4/a"
# categories = driver.find_elements(By.XPATH, categories_xpath)

# # Initialize a list to store data
# data = []

# for category in categories:
#     try:
#         category.click()
#         time.sleep(2)  # Wait for the content to load

#         # Step 3: Locate elements using the provided XPath for the current category
#         content_xpath = "/html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[1]/li"
#         elements = driver.find_elements(By.XPATH, content_xpath)

#         # Extract data from elements with the class "active"
#         for element in elements:
#             class_name = element.get_attribute("class")
#             if class_name and "active" in class_name:
#                 data.append(element.text)
#     except Exception as e:
#         print(f"Error processing category: {e}")

# # Create a DataFrame
# if data:
#     df = pd.DataFrame(data, columns=["Content"])

#     # Save DataFrame to an Excel file
#     output_path = "scraped_data.xlsx"
#     df.to_excel(output_path, index=False)
#     print(f"Data saved to {output_path}")
# else:
#     print("No active elements found.")

# # Close the WebDriver
# driver.quit()


# /html/body/div[3]/div[2]/div[2]/div[3]/h4/a
# /html/body/div[3]/div[2]/div[2]/div[3]/div/div/ul/ul[1]/li[1]
# /html/body/div[3]/div[2]/div[2]/div[3]/div/div/ul/ul[1]/li[9]


# /html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[4]/li[2]
# /html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[10]/li

# /html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[28]/li/text()

# /html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[9]/li[3]
# /html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[17]/li[10]
# /html/body/div[3]/div[2]/div[2]/div[1]/div/div/ul/ul[27]/li[3]

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configure Selenium WebDriver
options = Options()
# options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# service = Service('/path/to/chromedriver')  # Update with the correct path to your ChromeDriver

# Start the WebDriver
driver = webdriver.Chrome(options=options)

# Target URL
url = "https://reporterslab.org/fact-checking/#"
driver.get(url)

# Give the page some time to load
time.sleep(5)  # Adjust the sleep time as needed

# Step 1: Click the map view close button
map_view_close_xpath = "/html/body/div[4]/div/div[2]/div[3]/div[4]/div/div/a"
map_view_close_button = driver.find_element(By.XPATH, map_view_close_xpath)
map_view_close_button.click()

# Give some time for the page to update
time.sleep(2)

# Initialize a list to store data
data = []

# Step 2: Iterate through all categories dynamically
category_index = 1
while True:
    category_xpath = f"/html/body/div[3]/div[2]/div[2]/div[{category_index}]/h4/a"
    try:
        category = driver.find_element(By.XPATH, category_xpath)
        category.click()
        time.sleep(2)  # Wait for the content to load

        # Wait for all <ul> elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[3]/div[2]/div[2]/div[{category_index}]/div/div/ul"))
        )

        # Find all <ul> elements dynamically within the current category
        ul_elements = driver.find_elements(By.XPATH, f"/html/body/div[3]/div[2]/div[2]/div[{category_index}]/div/div/ul/ul")
        print(f"Number of <ul> elements in category[{category_index}]: {len(ul_elements)}")

        # Iterate through each <ul> and find all <li> elements
        for ul_index, ul_element in enumerate(ul_elements, start=1):
            li_elements = ul_element.find_elements(By.TAG_NAME, "li")
            print(f"Number of <li> elements in category[{category_index}] ul[{ul_index}]: {len(li_elements)}")

            # Append the text content of each <li> to the data list
            for li_index, li_element in enumerate(li_elements, start=1):
                li_text = li_element.text
                print(f"category[{category_index}] ul[{ul_index}] li[{li_index}]: {li_text}")
                data.append({"category_index": category_index, "ul_index": ul_index, "li_index": li_index, "content": li_text})

        category_index += 1  # Move to the next category

    except Exception as e:
        print(f"No more categories found at index {category_index}. Ending loop.")
        break

# Create a DataFrame
if data:
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file
    output_path = "scraped_li_content_all_categories.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")
else:
    print("No data found.")

# Close the WebDriver
driver.quit()



# /html/body/div[3]/div[2]/div[2]/div[3]/h4/a