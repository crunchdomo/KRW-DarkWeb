from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS
from urllib.parse import quote
import spacy

# Initialize spaCy for NER and the RDF Graph
nlp = spacy.load("en_core_web_sm")
g = Graph()

# Define your namespaces
dw = Namespace("http://darkwebisspooky/")

# Define the Location class
location_class = dw.Location

# Initialize spaCy NER
nlp = spacy.load("en_core_web_sm")

def is_valid_location(text):
    # Use spaCy NER to check if the text is a location
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:
            # Further filter out any non-location entities that might be incorrectly recognized
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

def add(subject, predicate, object, is_money=False, is_location=False):
    # Normalize object for URI if it's a location
    if is_location and object not in ["-", "Worldwide"]:
        object = quote(object.replace(" ", "_").replace("\\n", "").replace("'", ""))
        if is_valid_location(object):
            location_uri = dw[object]
            g.add((location_uri, RDF.type, location_class))
            g.add((subject, predicate, location_uri))
        else:
            # If not a valid location, add as a literal (or handle differently)
            g.add((subject, predicate, Literal(object)))
    elif is_money and object != "-":
        # Handle money extraction
        extracted_prices = extract_price_from_text(object)
        if extracted_prices:
            object = extracted_prices[0].replace('$', '')
        g.add((subject, predicate, Literal(object)))
    else:
        # Add all other triples as literals
        g.add((subject, predicate, Literal(object)))

# Process the SQL file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Datasets\\DreamMarket 2016\\DreamMarket_2016\\DreamMarket2016_product.sql', 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith('INSERT INTO `dnm_dream` VALUES'):
            values = line.split('VALUES')[1].strip().strip(';').strip('(').strip(')').split(',', 3)
            last_values = clean_and_split_values(values[-1])
            all_values = values[:-1] + last_values
            
            product_uri = URIRef(dw['product/' + all_values[0].strip()])
            
            # Add product information to the graph
            add(product_uri, RDF.type, dw.Product)
            add(product_uri, dw.productName, all_values[1].strip().strip("'"))
            add(product_uri, dw.category, all_values[2].strip().strip("'"))
            add(product_uri, dw.description, all_values[3].strip().strip("'").replace("\\n", "\n"), is_money=True)
            add(product_uri, dw.sellerName, all_values[6].strip().strip("'"))
            add(product_uri, dw.price, all_values[7].strip().strip("'"), is_money=True)
            add(product_uri, dw.keywords, all_values[5].strip().strip("'"))
            add(product_uri, dw.ship_from, all_values[15].strip().strip("'").replace("\\n", "\n"), is_location=True)
            add(product_uri, dw.ship_to, all_values[16].strip().strip("'").replace("\\n", "\n"), is_location=True)
            add(product_uri, dw.shipping_option, all_values[4].strip().strip("'"))
            add(product_uri, dw.market_name, all_values[14].strip().strip("'"))

# Serialize the graph
g.serialize(destination='fooo.ttl', format='turtle')
