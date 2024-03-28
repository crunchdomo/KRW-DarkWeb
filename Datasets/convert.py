from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS
from urllib.parse import quote, unquote
import re
import spacy

# Initialize the RDF Graph
g = Graph()

# Define your namespaces
dw = Namespace("http://darkwebisspooky/")

# Initialize spaCy NER
nlp = spacy.load("en_core_web_sm")

# Object property definitions
hasSeller = dw.hasSeller
belongsToCategory = dw.belongsToCategory
shipsFrom = dw.shipsFrom
shipsTo = dw.shipsTo

# Define the Location class
location_class = dw.Location

def clean_data(value_str):
    # Decode URL-encoded strings
    decoded_str = unquote(value_str)
    # Remove unwanted characters and trailing numbers
    cleaned_str = re.sub(r"[\n\t]+", " ", decoded_str).strip()
    cleaned_str = re.sub(r"%[0-9A-Fa-f]{2}", "", cleaned_str)  # Remove URL-encoded chars
    cleaned_str = re.sub(r"\\n", " ", cleaned_str)  # Replace escaped newlines with space
    # Further clean-up as needed
    cleaned_str = re.sub(r"_[\d]+", "", cleaned_str)  # Remove trailing numbers prefixed with _
    return cleaned_str

def clean_and_split_values(value_str):
    values = value_str.strip().strip('(').strip(')').split("',")
    values = [v.strip("'") for v in values]
    return values


def create_or_get_class(name, is_location=False):
    clean_name = clean_data(name)
    # Normalize name to create a valid URI
    name_uri = quote(clean_name.replace(" ", "_").replace("'", ""))
    class_uri = dw[name_uri]
    
    # Check if the class already exists, if not, create it
    if (class_uri, None, None) not in g:
        g.add((class_uri, RDF.type, RDFS.Class))
        g.add((class_uri, RDFS.label, Literal(clean_name)))
        if is_location:
            # Mark it as a subclass of Location
            g.add((class_uri, RDF.type, location_class))
    return class_uri

def add(subject, predicate, object, is_object_property=False):
    if is_object_property:
        g.add((subject, predicate, URIRef(object)))
    else:
        g.add((subject, predicate, Literal(object)))

# Process the SQL file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Datasets\\DreamMarket 2016\\DreamMarket_2016\\DreamMarket2016_product.sql', 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith('INSERT INTO `dnm_dream` VALUES'):
            values = line.split('VALUES')[1].strip().strip(';').strip('(').strip(')').split(',', 3)
            last_values = clean_and_split_values(values[-1])
            all_values = values[:-1] + last_values
            
            product_uri = URIRef(dw['product/' + all_values[0].strip()])
            
            # Create or get the class for the product category
            category_class = create_or_get_class(all_values[2].strip().strip("'"), is_location=False)
            
            # Add product information to the graph with object properties
            g.add((product_uri, RDF.type, category_class))
            add(product_uri, dw.productName, all_values[1].strip().strip("'"))
            add(product_uri, dw.description, all_values[3].strip().strip("'").replace("\\n", "\n"))
            add(product_uri, dw.price, all_values[7].strip().strip("'"))
            
            # Object property assertions
            seller_uri = URIRef(dw['seller/' + all_values[6].strip().strip("'")])
            add(product_uri, hasSeller, seller_uri, is_object_property=True)
            
            # Clean the locations and create location classes
            ship_from_location = create_or_get_class(all_values[15].strip().strip("'"), is_location=True)
            ship_to_location = create_or_get_class(all_values[16].strip().strip("'"), is_location=True)
            
            # Link product to its shipping information with object properties
            add(product_uri, shipsFrom, ship_from_location, is_object_property=True)
            add(product_uri, shipsTo, ship_to_location, is_object_property=True)

# Serialize the graph
g.serialize(destination='bhyunkg.ttl', format='turtle')
