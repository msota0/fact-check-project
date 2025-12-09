import pandas as pd

# Load the Excel files (replace 'file1.xlsx' and 'file2.xlsx' with actual file paths)
df1 = pd.read_csv("./google_sources_scraped/combined_factcheck_sources_unique.csv")  # Adjust sheet_name if needed
df2 = pd.read_excel("./raw/news_fact_checker_websites_with_urls.xlsx", sheet_name="Sheet1")  # Adjust sheet_name if needed

# Specify the column names to compare
field1 = "Fact Check Text"  # Change to the actual column name in df1
field2 = "content"  # Change to the actual column name in df2

# Convert the selected columns to sets (handle NaN values by dropping them)
set1 = set(df1[field1].dropna())
set2 = set(df2[field2].dropna())

# Find common values
common_values = set1.intersection(set2)

# Display the result
print("Common values:", common_values)

# Optionally, save results to a new Excel file
output_df = pd.DataFrame({"Common Values": list(common_values)})
output_df.to_excel("common_values.xlsx", index=False)
print("Common values saved to 'common_values.xlsx'")
