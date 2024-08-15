def merge_tab_separated_files_with_single_header(file1_path, file2_path, file3_path, output_path):
    # Read the first file
    with open(file1_path, 'r') as file1:
        content1 = file1.readlines()
    
    # Read the second file
    with open(file2_path, 'r') as file2:
        content2 = file2.readlines()
    
    # Read the third file
    with open(file3_path, 'r') as file3:
        content3 = file3.readlines()

    # Separate headers and data
    header1, data1 = content1[0], content1[1:]
    header2, data2 = content2[0], content2[1:]
    header3, data3 = content3[0], content3[1:]

    # Ensure all files have the same header
    if header1 != header2 or header1 != header3:
        raise ValueError("Headers do not match!")

    # Define the index of the ID column
    id_column_index = header1.split('\t').index('ID')

    # Standardize the formatting of the ID column values
    def format_id_column(data):
        formatted_data = []
        for line in data:
            columns = line.strip().split('\t')
            # Remove trailing ".0" from ID column value, if present
            columns[id_column_index] = columns[id_column_index].split('.')[0]
            formatted_data.append('\t'.join(columns))
        return formatted_data

    # Format the ID column in all data
    data1 = format_id_column(data1)
    data2 = format_id_column(data2)
    data3 = format_id_column(data3)

    # Combine the content
    combined_content = [header1.strip()]

    # Add tab-separated data
    combined_content.extend(data1)
    combined_content.extend(data2)
    combined_content.extend(data3)

    # Write the combined content to the output file
    with open(output_path, 'w') as output_file:
        output_file.writelines('\n'.join(combined_content))

# Example usage
file1_path = r'C:\Users\maxpa\Documents\AMaster\MasterThesis\ARGUS2\ARGUS\misc\data\split\Missingfrompart2_3.txt'
file2_path = r'C:\Users\maxpa\Documents\AMaster\MasterThesis\ARGUS2\ARGUS\misc\data\split\URLs_part4.txt'
file3_path = r'C:\Users\maxpa\Documents\AMaster\MasterThesis\ARGUS2\ARGUS\misc\data\split\Missingfrompart1.txt'
output_path = r'C:\Users\maxpa\Documents\AMaster\MasterThesis\ARGUS2\ARGUS\misc\data\split\URLS4_rest.txt'

merge_tab_separated_files_with_single_header(file1_path, file2_path, file3_path, output_path)
