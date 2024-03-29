from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL
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
    cleaned_str = unquote(value_str)

    parts = cleaned_str.split('),(')
    if len(parts) > 1:
        # This is a simplistic approach; you might need more sophisticated logic
        cleaned_str = parts[0]  # Consider more complex logic for choosing the correct part

    # Specific replacement cause this is jus tthe easiest way to sort out stuff
    # Short ones go first so they dont accidentaly replace some letters later with a new place

    cleaned_str = re.sub(r"WW", "", cleaned_str)
    cleaned_str = re.sub(r"EU", "Europe", cleaned_str)
    cleaned_str = re.sub(r"UK", "United_Kingdom", cleaned_str)
    cleaned_str = re.sub(r"USA", "United_States", cleaned_str)
    cleaned_str = re.sub(r"US", "United_States", cleaned_str)

    cleaned_str = re.sub(r"canada", "Canada", cleaned_str)
    cleaned_str = re.sub(r"worldwide", "Worldwide", cleaned_str)
    cleaned_str = re.sub(r"Worldwide Worldwide", "Worldwide", cleaned_str)
    cleaned_str = re.sub(r"Belgium and the Netherlands", "Belgium Netherlands", cleaned_str)
    cleaned_str = re.sub(r"United Kingdom", "United_Kingdom", cleaned_str)
    cleaned_str = re.sub(r"United States", "United_States", cleaned_str)
    return cleaned_str.strip()

def clean_data(value_str):
    # Initial clean-up: Decode URL-encoded strings and remove unwanted characters
    decoded_str = unquote(value_str)
    cleaned_str = re.sub(r"Digital Goods", "Digital_Goods", decoded_str)
    parts = cleaned_str.split(' ')
    
    if len(parts) > 1:
        cleaned_str = parts[0]
    if cleaned_str.startswith("\\n\\n"):
        cleaned_str = "-"
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
with open('Datasets\\DreamMarket_2016\\DreamMarket2016_product.sql', 'r', encoding='utf-8') as file:
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
            seller_uri = clean_data(all_values[6].strip().strip("'"))
            add(product_uri, hasSeller, seller_uri, is_object_property=True)
            
            # Clean the locations and create location classes
            ship_from_location = clean_location(all_values[15].strip().strip("'"))
            ship_to_location = clean_location(all_values[16].strip().strip("'"))
            for start in ship_from_location.split(' '):
                ship_from_uri = create_or_get_class(start, is_location=True)
                add(product_uri, shipsFrom, ship_from_uri, is_object_property=True)
                
            for stop in ship_to_location.split(' '):
                ship_to_uri = create_or_get_class(stop, is_location=True)
                add(product_uri, shipsTo, ship_to_uri, is_object_property=True)
                
                
            g.add((hasSeller, RDF.type, OWL.ObjectProperty))
            g.add((shipsFrom, RDF.type, OWL.ObjectProperty))
            g.add((shipsTo, RDF.type, OWL.ObjectProperty))
            g.add((belongsToCategory, RDF.type, OWL.ObjectProperty))


# Serialize the graph
g.serialize(destination='DMProducts2016.ttl', format='turtle')
