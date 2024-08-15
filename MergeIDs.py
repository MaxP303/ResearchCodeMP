import csv

# Standardize the formatting of the ID column values
def format_id_column(id_value):
    return id_value.split('.')[0]

# Process and merge data from both CSV files
def process_and_merge_files(first_file_path, second_file_path, final_output_path):
    with open(first_file_path, 'r') as first_file, open(second_file_path, 'r') as second_file, open(final_output_path, 'w', newline='') as output_file:
        first_reader = csv.DictReader(first_file)
        second_reader = csv.DictReader(second_file)
        
        fieldnames = ['ID', 'Latitude', 'Longitude', 'total_oi', 'total_ce']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        # Create a dictionary from the second file for quick lookup by ID
        second_data = {format_id_column(row['ID']): row for row in second_reader}

        for row in first_reader:
            row['ID'] = format_id_column(row['ID'])
            if row['Latitude'] and row['Longitude']:
                matching_row = second_data.get(row['ID'])
                row_to_write = {
                    'ID': row['ID'],
                    'Latitude': row['Latitude'],
                    'Longitude': row['Longitude'],
                    'total_oi': matching_row.get('total_oi', '') if matching_row else '',
                    'total_ce': matching_row.get('total_ce', '') if matching_row else ''
                }

                # Check if all values are present and non-empty before writing the row
                if all(row_to_write.values()):
                    writer.writerow(row_to_write)

# File paths
# File paths
first_input_file = r"C:\Users\maxpa\Documents\AMaster\MasterThesis\ARGUS2\ARGUS\misc\data\Thesis_Data_no_dupli.csv"
second_input_file = r'D:\Documents\ThesisD\Cronbach_trimmed_datafinal.csv'
final_output_file = r"D:\Documents\ThesisD\Cronbach_trimmed_geodatafinal.csv"

# Process and merge the data
process_and_merge_files(first_input_file, second_input_file, final_output_file)
