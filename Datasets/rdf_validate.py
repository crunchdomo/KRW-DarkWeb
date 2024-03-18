from rdflib import Graph

# Initialize a graph
g = Graph()

# Parse RDF data from a file
try:
    g.parse("C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\fooo.ttl", format="turtle")
    print("RDF data is valid and has been successfully parsed.")
except Exception as e:
    print(f"An error occurred while parsing the RDF data: {e}")

# Print the number of triples in the RDF graph
print(f"Number of triples in the RDF graph: {len(g)}")