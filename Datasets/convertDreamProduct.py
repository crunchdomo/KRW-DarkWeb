from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS
from urllib.parse import quote, unquote
import re
import spacy

# Initialize the RDF Graph
g = Graph()

# Define your namespaces
dw = Namespace("http://darkwebisspooky/")

# Define the Location class
location_class = dw.Location

# Object property definitions
hasSeller = dw.hasSeller
belongsToCategory = dw.belongsToCategory
shipsFrom = dw.shipsFrom
shipsTo = dw.shipsTo

# Initialize spaCy NER
nlp = spacy.load("en_core_web_sm")

def is_valid_location(text):
    # Use spaCy NER to check if the text is a location
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:
            if ent.text not in ["-", "Worldwide", "Europe Worldwide", "Worldwide Europe"]:
                return True
    return False

def extract_price_from_text(text):
    doc = nlp(text)
    prices = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
    return prices if prices else None

def clean_and_split_values(value_str):
    values = value_str.strip().strip('(').strip(')').split("',")
    values = [v.strip("'") for v in values]
    return values

def add(subject, predicate, object, is_object_property=False):
    if is_object_property:
        # If the predicate is an object property, add the object as a URIRef
        g.add((subject, predicate, URIRef(object)))
    else:
        # For data properties, add the object as a Literal
        g.add((subject, predicate, Literal(object)))

def clean_location(value_str):
    # Decode URL-encoded strings and remove unwanted characters
    decoded_str = unquote(value_str)
    # Initial clean-up to remove URL-encoded chars and replace escaped newlines with space
    cleaned_str = re.sub(r"%[0-9A-Fa-f]{2}", "", decoded_str)  # Remove URL-encoded chars
    cleaned_str = re.sub(r"\\n", " ", cleaned_str)  # Replace escaped newlines with space
    cleaned_str = cleaned_str.strip()

    # Specific clean-up based on observed patterns
    # Example: Split concatenated names and select the first, or apply other logic as needed
    parts = cleaned_str.split('_')
    if len(parts) > 1:
        # This is a simplistic approach; you might need more sophisticated logic
        cleaned_str = parts[0]  # Consider more complex logic for choosing the correct part

    # Further refine the cleaning process as needed based on the patterns in your data
    # Example: Remove trailing numbers and other unwanted substrings
    cleaned_str = re.sub(r"\d+$", "", cleaned_str)  # Remove trailing digits
    cleaned_str = re.sub(r"Worldwide Worldwide", "Worldwide", cleaned_str)  # Example specific replacement

    return cleaned_str.strip()

def clean_data(value_str):
    # Initial clean-up: Decode URL-encoded strings and remove unwanted characters
    decoded_str = unquote(value_str)
    cleaned_str = re.sub(r"[\n\t]+", " ", decoded_str).strip()
    cleaned_str = re.sub(r"%[0-9A-Fa-f]{2}", "", cleaned_str)  # Remove URL-encoded chars
    cleaned_str = re.sub(r"\\n", " ", cleaned_str)  # Replace escaped newlines with space
    # Further clean-up as needed
    # Example: Remove any unexpected concatenated values or characters
    cleaned_str = re.sub(r"_[\d]+", "", cleaned_str)  # Remove trailing numbers prefixed with _
    return cleaned_str

def create_or_get_class(name, is_location=False):
    clean_name = clean_location(name) if is_location else clean_data(name)
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

# Process the SQL file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Datasets\\DreamMarket 2016\\DreamMarket_2016\\DreamMarket2016_product.sql', 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith('INSERT INTO `dnm_dream` VALUES'):
            values = line.split('VALUES')[1].strip().strip(';').strip('(').strip(')').split(',', 3)
            last_values = clean_and_split_values(values[-1])
            all_values = values[:-1] + last_values
            
            product_uri = URIRef(dw['product/' + all_values[0].strip()])
            
            # Create or get the class for the product category
            category_class = create_or_get_class(all_values[2].strip().strip("'"))
            
            # Add product information to the graph with object properties
            g.add((product_uri, RDF.type, category_class))
            add(product_uri, dw.productName, all_values[1].strip().strip("'"))
            add(product_uri, dw.description, all_values[3].strip().strip("'").replace("\\n", "\n"))
            add(product_uri, dw.price, all_values[7].strip().strip("'"))
            
            # Object property assertions
            seller_uri = URIRef(dw['seller/' + all_values[6].strip().strip("'")])
            add(product_uri, hasSeller, seller_uri, is_object_property=True)
            
            # Clean the locations and create location classes
            ship_from_location = clean_location(all_values[15].strip().strip("'"))
            ship_to_location = clean_location(all_values[16].strip().strip("'"))
            
            ship_from_uri = create_or_get_class(ship_from_location, is_location=True)
            ship_to_uri = create_or_get_class(ship_to_location, is_location=True)
            
            # Link product to its shipping information with object properties
            add(product_uri, shipsFrom, ship_from_uri, is_object_property=True)
            add(product_uri, shipsTo, ship_to_uri, is_object_property=True)

# Serialize the graph
g.serialize(destination='ajjfdslkdsflkfdsklfdslkfdslk.ttl', format='turtle')
