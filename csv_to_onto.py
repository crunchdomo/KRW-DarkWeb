import csv
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

# Initialize a graph
g = Graph()

# Define your namespace
n = Namespace("https://interpol-innovation-centre.github.io/DW-VA-Taxonomy/taxonomies/abuses#")

# Open the CSV file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Interpol\\abuses.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Create a URI for each abuse type
        abuse = URIRef(row['uri'])
        
        # Add types and labels
        g.add((abuse, RDF.type, RDFS.Class))
        g.add((abuse, RDFS.label, Literal(row['label'])))
        g.add((abuse, RDFS.comment, Literal(row['description'])))
        
# Serialize the graph in RDF/XML format
with open('abuses.owl', 'w') as output_file:
    output_file.write(g.serialize(format='xml'))
