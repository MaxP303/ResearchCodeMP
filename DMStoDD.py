import pandas as pd
import re

# Function to convert DMS to Decimal Degrees
def dms_to_dd(dms):
    # Extract the degrees, minutes, and seconds using regex
    parts = re.split('[°\'" ]+', dms.strip())
    
    # Convert parts to float and assign sign based on direction
    degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    direction = parts[3]

    # Calculate the decimal degree
    dd = degrees + (minutes / 60) + (seconds / 3600)
    
    # Make the result negative if the direction is South or West
    if direction in ['S', 'W']:
        dd = -dd
    
    return dd

# Load the CSV file
df = pd.read_csv(r"D:\Documents\ThesisD\Cronbach_trimmed_geodatafinal.csv")

# Convert Latitude and Longitude in place
df['Latitude'] = df['Latitude'].apply(dms_to_dd)
df['Longitude'] = df['Longitude'].apply(dms_to_dd)

# Save the updated DataFrame to a new CSV file
df.to_csv(r"D:\Documents\ThesisD\Cronbach_trimmed_geodatafinalDD.csv", index=False)

print(df.head())
