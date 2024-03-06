from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF

# Create an RDF Graph
g = Graph()

# Define a custom namespace
ns = Namespace("http://example.org/")

# Define a namespace for your ontology/vocabulary
vocab = Namespace("http://example.org/vocab/")

# Function to clean and split SQL values, considering potential commas within the values
def clean_and_split_values(value_str):
    # This is a simplified approach and might not work for all cases
    # Ideally, use a more robust method to parse SQL values, especially if values contain commas
    values = value_str.strip().strip('(').strip(')').split("',")
    values = [v.strip("'") for v in values]
    return values

# Load SQL data into the graph
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Datasets\\DreamMarket 2016\\DreamMarket_2016\\DreamMarket2016_product.sql', 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith('INSERT INTO `dnm_dream` VALUES'):
            # Remove the INSERT INTO statement and split the values
            values = line.split('VALUES')[1].strip().strip(';').strip('(').strip(')').split(',', 3)
            # Further split the last part to handle longtext fields correctly
            last_values = clean_and_split_values(values[-1])
            all_values = values[:-1] + last_values
            
            # Create a new subject URI for this entry
            product_uri = URIRef(ns['product/' + all_values[0].strip()])
            
            # Add triples using the values. Adjust indices based on actual SQL data
            g.add((product_uri, RDF.type, vocab.Product))
            g.add((product_uri, vocab.productName, Literal(all_values[1].strip().strip("'"))))
            g.add((product_uri, vocab.category, Literal(all_values[2].strip().strip("'"))))
            g.add((product_uri, vocab.description, Literal(all_values[3].strip().strip("'").replace("\\n", "\n"))))
            g.add((product_uri, vocab.sellerName, Literal(all_values[6].strip().strip("'"))))
            g.add((product_uri, vocab.price, Literal(all_values[7].strip().strip("'"))))

# Serialize the graph to RDF/TTL format
g.serialize(destination='output.ttl', format='turtle')
