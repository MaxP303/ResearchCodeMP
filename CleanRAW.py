import os
import pandas as pd

# Define the directory containing all CSV files
directory = r"C:\yourpath\data\rawdata"

# Create an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Initialize the starting ID
current_max_id = 0

# Loop through all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Read each ; separated CSV file into a DataFrame
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath, sep=';', na_values=['N/A', 'na', 'NA', 'n.a.'], on_bad_lines='skip')
        
        # Remove dots from the first column, convert to numeric
        #df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.replace('.', '', regex=False)
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        
        # Adjust IDs to ensure they continue from the last file
        df.iloc[:, 0] = df.iloc[:, 0] + current_max_id
        
        # Update the current max ID
        current_max_id = df.iloc[:, 0].max()
        
        # Append the DataFrame to the combined DataFrame
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# Remove missing values from specific columns, for example, 'Website address'
specific_columns = ['Website address']  # Replace with all column names, comma separated
combined_df_cleaned = combined_df.dropna(subset=specific_columns)

# Rename the 'Website address' column to 'URL'
combined_df_cleaned = combined_df_cleaned.rename(columns={'Website address': 'URL'})

# Rename the first column to 'ID'
combined_df_cleaned = combined_df_cleaned.rename(columns={combined_df_cleaned.columns[0]: 'ID'})

# Save the cleaned DataFrame to a .csv file
combined_df_cleaned.to_csv(r"C:\Users\maxpa\Documents\AMaster\MasterThesis\ARGUS2\ARGUS\misc\data\Thesis_Data.csv", index=False)
