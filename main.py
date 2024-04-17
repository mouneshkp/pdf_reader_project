import pdfplumber
import csv
import re

# Define regular expressions for extracting specific patterns
header_pattern = r'(Name|Invoice No\.|PNR|GSTIN):(.+)'  # Matches Name, Invoice No., PNR, GSTIN followed by their values
table_pattern = r'Passenger Fare|Airport tax|Excess Baggage|ADV Pax Info Fee|C Fee|W Fee|Meal|Penalty|Seat Selection Fee|Insurance|Misc Fee'  # Matches rows in the table

# Initialize CSV data list with the header
csv_data = [['Name', 'Invoice Number', 'PNR', 'GSTIN', 'Total Amount', 'CGST', 'SGST', 'IGST', 'Total Invoice value']]

# Process each PDF file
for file_num in range(1, 6):
    with pdfplumber.open(f"pdf{file_num}.pdf") as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        
        # Extract header data using regular expressions
        header_data = dict(re.findall(header_pattern, text, re.IGNORECASE))
        
        # Extract table data using regular expressions
        table_data = []
        for line in text.split('\n'):
            if re.search(table_pattern, line):
                table_data.append(line.split())
        
        # Combine header and table data
        combined_data = [header_data.get(key, '') for key in csv_data[0][:4]]  # Get header values from the dictionary
        combined_data += [row[-1] for row in table_data if len(row) > 1]  # Add last value from each table row
        
        # Append combined data to CSV data list
        csv_data.append(combined_data)



# Write CSV data to a file
with open('output_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)





