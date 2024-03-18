import csv
import yaml

# Load the YAML file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Interpol\\DW-VA-Taxonomy-master\\_data\\entities.yaml', 'r', encoding='utf-8') as yaml_file:
    data = yaml.safe_load(yaml_file)

# Open a new CSV file for writing with UTF-8 encoding
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Interpol\\DW-VA-Taxonomy-master\\_data\\entities_new.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header row
    writer.writerow(['id', 'prefLabel', 'type', 'description', 'broader'])
    
    # Write data rows
    for key, value in data.items():
        if key != 'scheme':  # Skip the scheme information
            writer.writerow([value.get('id', ''),
                             value.get('prefLabel', ''),
                             value.get('type', ''),
                             value.get('description', '').replace('\n', ' '),  # Remove newlines in descriptions
                             value.get('broader', '')])
