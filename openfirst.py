import pandas as pd

# Step 1: Read the first 2.000 rows
file_path = r"C:\yourpath\data\rawdata\data.csv"
df = pd.read_csv(file_path, nrows=2000)

# Step 2: Save to a new CSV file
output_file_path = r"C:\yourpath\data\first2000_data.csv"
df.to_csv(output_file_path, index=False)
