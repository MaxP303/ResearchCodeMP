import pandas as pd

# Step 1: Read the first 100,000 rows
file_path = r"D:\Documents\ThesisD\counted_nodupli_datafinal2_1.csv"
df = pd.read_csv(file_path, nrows=2000)

# Step 2: Save to a new CSV file
output_file_path = r"D:\Documents\ThesisD\first2000with_outliers_data.csv"
df.to_csv(output_file_path, index=False)