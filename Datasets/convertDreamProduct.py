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

def create_or_get_class(category):
    # Decode URL-encoded strings
    decoded_category = unquote(category)
    # Remove newline, tab characters, and trailing numbers from the category string
    clean_category = re.sub(r"[\n\t]+", " ", decoded_category).strip()
    clean_category = re.sub(r"\s+\d+$", "", clean_category)
    
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
            
            ship_from_uri = URIRef(dw['location/' + quote(all_values[15].strip().strip("'").replace(" ", "_"))])
            add(product_uri, shipsFrom, ship_from_uri, is_object_property=True)
            
            ship_to_uri = URIRef(dw['location/' + quote(all_values[16].strip().strip("'").replace(" ", "_"))])
            add(product_uri, shipsTo, ship_to_uri, is_object_property=True)

# Serialize the graph
g.serialize(destination='fjamsmsmsmsm.ttl', format='turtle')
