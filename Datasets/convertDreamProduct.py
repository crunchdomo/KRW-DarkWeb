from rdflib import Graph, Literal, Namespace, URIRef, RDF
import spacy

# Initialize spaCy for NER and the RDF Graph
nlp = spacy.load("en_core_web_sm")
g = Graph()

# Define your namespaces
dw = Namespace("http://darkwebisspooky/")
vocab = Namespace("http://example.org/vocab/")

def extract_price_from_text(text):
    doc = nlp(text)
    prices = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
    return prices if prices else None

def extract_locations_from_text(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
    return locations

def clean_and_split_values(value_str):
    values = value_str.strip().strip('(').strip(')').split("',")
    values = [v.strip("'") for v in values]
    return values

def add(subject, predicate, object, is_money=False, is_location=False):
    if is_money:
        extracted_prices = extract_price_from_text(object)
        if extracted_prices:
            object = extracted_prices[0].replace('$', '')  # Remove the dollar sign
    elif is_location:
        extracted_locations = extract_locations_from_text(object)
        if extracted_locations:
            for location in extracted_locations:
                g.add((subject, predicate, Literal(location)))
            return  # Skip adding the original object if locations were added
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
g.serialize(destination='final_output.ttl', format='turtle')