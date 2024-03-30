from rdflib import Graph, OWL, RDF, RDFS, Literal

# Load the 2016 ontology
g2016 = Graph()
g2016.parse(r"C:\Users\oenfa\Documents\GitHub\KRW-DarkWeb\DreamMarket_2016_V2.rdf", encoding='utf-8', format="owl")

# Load the 2017 ontology
g2017 = Graph()
g2017.parse(r"C:\Users\oenfa\Documents\GitHub\KRW-DarkWeb\DreamMarket_2017_V2.rdf", encoding='utf-8', format="owl")

# Create a new graph for the merged ontology
merged_graph = Graph()

# Merge the graphs
for stmt in g2016:
    merged_graph.add(stmt)
for stmt in g2017:
    merged_graph.add(stmt)

# Assuming you have a way to identify the same entities across ontologies,
# you would add owl:sameAs statements for them here.
# For example:
# merged_graph.add((entity_from_g2016, OWL.sameAs, entity_from_g2017))

# Serialize the merged graph
merged_graph.serialize(destination="merged_ontology.ttl", format="turtle")