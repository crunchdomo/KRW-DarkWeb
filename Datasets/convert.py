from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, FOAF

# Create an RDF Graph
g = Graph()

# Define a custom namespace
ns = Namespace("http://example.org/")

# Define a namespace for your ontology/vocabulary
vocab = Namespace("http://example.org/vocab/")

# Load SQL data into the graph
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Datasets\\DreamMarket 2017\\DreamMarket_2017\\DreamMarket2017_seller.sql', 'r') as file:
    for line in file:
        if line.startswith('INSERT INTO `dnm_dream` VALUES'):
            # Remove the INSERT INTO statement and split the values
            values = line.split('VALUES')[1].strip().strip(';').strip('(').strip(')').split(',')
            
            # Create a new subject URI for this entry
            seller_uri = URIRef(ns['seller/' + values[0].strip()])
            
            # Add triples using the values. You may need to adjust indices based on actual SQL data
            g.add((seller_uri, RDF.type, vocab.Seller))
            g.add((seller_uri, FOAF.name, Literal(values[1].strip().strip("'"))))
            g.add((seller_uri, vocab.memberSince, Literal(values[2].strip().strip("'"))))
            
            # Add description
            # Assuming the description is in the 7th position (index 6) in your values list
            description = values[7].strip().strip("'").replace("\\n", "\n")  # Handling escaped newlines
            g.add((seller_uri, vocab.description, Literal(description)))
            
            # Continue for other fields as needed

# Serialize the graph to RDF/TTL format
g.serialize(destination='output.ttl', format='turtle')
