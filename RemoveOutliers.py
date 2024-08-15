import pandas as pd
import numpy as np

input_path = r"D:\Documents\ThesisD\first2000with_outliers_data.csv"
df = pd.read_csv(input_path)

def trim_upper(df, column_name, upper_percent):
    # Calculate the quantile that corresponds to the upper_percent
    upper_threshold = df[column_name].quantile(1 - upper_percent)
    
    # Filter out rows where the value in the column exceeds the upper_threshold
    df_trimmed = df[df[column_name] <= upper_threshold]
    
    return df_trimmed

# Trim the top 0.5 percent of the columns 'total_oi' and 'total_ce'
upper_percent = 0.005  # Trim the top 0.5%
df = trim_upper(df, 'total_oi', upper_percent)
df = trim_upper(df, 'total_ce', upper_percent)

# Save the trimmed DataFrame
output_path = r"D:\Documents\ThesisD\first2000no_outliers_data.csv"
df.to_csv(output_path, index=False)
