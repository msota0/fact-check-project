import pandas as pd
import glob

# Define the path where the 11 CSV files are located
file_path = "./individuals/"  # Ensure the path ends with a slash
csv_files = glob.glob(file_path + "*.csv")  # Get all CSV files in the directory

# Check if files are found
if not csv_files:
    print("No CSV files found. Please check the directory path.")
else:
    print(f"Found {len(csv_files)} files: {csv_files}")

# Initialize an empty DataFrame
combined_df = pd.DataFrame()

# Read and combine all CSV files
for file in csv_files:
    try:
        df = pd.read_csv(file)  # Read each CSV file
        combined_df = pd.concat([combined_df, df], ignore_index=True)  # Stack rows
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Drop duplicates based on the 'Fact Check Text' column
if not combined_df.empty:
    combined_df = combined_df.drop_duplicates(subset=['Fact Check Text'])

    # Save the combined DataFrame to a new CSV file
    output_file = "combined_factcheck_sources_unique.csv"
    combined_df.to_csv(output_file, index=False)
    print(len(combined_df))
    print(f"Combined file saved as '{output_file}'.")
else:
    print("The combined DataFrame is empty. Please check the input files.")
