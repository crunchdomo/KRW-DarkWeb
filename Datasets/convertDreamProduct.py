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


def clean_data(value_str):
    # Decode URL-encoded strings
    decoded_str = unquote(value_str)
    # Additional cleaning steps, e.g., removing unwanted characters
    cleaned_str = re.sub(r"[\n\t]+", " ", decoded_str).strip()
    cleaned_str = re.sub(r"\s+\d+$", "", cleaned_str)  # Example: remove trailing numbers
    return cleaned_str

def process_sql_line(line):
    # Example of processing an SQL line
    # This is a placeholder; adjust according to your actual data format
    values = line.split('VALUES')[1].strip().strip(';').strip('(').strip(')').split(',', 3)
    last_values = clean_and_split_values(values[-1])
    all_values = values[:-1] + last_values
    
    # Clean and decode each value as needed
    for i, value in enumerate(all_values):
        all_values[i] = clean_data(value)
        
        
def create_location_class(location):
    # Decode URL-encoded strings and clean the location name
    decoded_location = unquote(location)
    clean_location = re.sub(r"[\n\t]+", " ", decoded_location).strip()
    clean_location = re.sub(r"\s+\d+$", "", clean_location)
    
    # Normalize location to create a valid URI
    location_uri = quote(clean_location.replace(" ", "_").replace("'", ""))
    class_uri = dw[location_uri]
    
    # Check if the class already exists, if not, create it
    if (class_uri, None, None) not in g:
        g.add((class_uri, RDF.type, RDFS.Class))
        g.add((class_uri, RDF.type, location_class))  # Mark it as a subclass of Location
        g.add((class_uri, RDFS.label, Literal(clean_location)))
    return class_uri


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

def clean_category_name(category):
    # Decode URL-encoded strings
    decoded_category = unquote(category)
    # Remove unwanted characters and trailing numbers
    clean_category = re.sub(r"[\n\t]+", " ", decoded_category).strip()
    clean_category = re.sub(r"\s+\d+$", "", clean_category)
    return clean_category

def create_or_get_class(category):
    clean_category = clean_category_name(category)
    # Normalize category to create a valid URI
    category_uri = quote(clean_category.replace(" ", "_").replace("'", ""))
    class_uri = dw[category_uri]
    # Check if the class already exists, if not, create it
    if (class_uri, None, None) not in g:
        g.add((class_uri, RDF.type, RDFS.Class))
        g.add((class_uri, RDFS.label, Literal(clean_category)))
    return class_uri


# Process the SQL file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Datasets\\DreamMarket 2016\\DreamMarket_2016\\DreamMarket2016_product.sql', 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith('INSERT INTO `dnm_dream` VALUES'):
            process_sql_line(line)
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
            
            # Create location classes and add object property assertions
            ship_from_location = create_location_class(all_values[15].strip().strip("'"))
            add(product_uri, shipsFrom, ship_from_location, is_object_property=True)
            
            ship_to_location = create_location_class(all_values[16].strip().strip("'"))
            add(product_uri, shipsTo, ship_to_location, is_object_property=True)


# Serialize the graph
g.serialize(destination='momoamama.ttl', format='turtle')
