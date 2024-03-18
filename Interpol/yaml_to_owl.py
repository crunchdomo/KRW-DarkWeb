import yaml
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS

# Load the YAML file
with open('C:\\Users\\oenfa\\Documents\\GitHub\\KRW-DarkWeb\\Interpol\\DW-VA-Taxonomy-master\\_data', 'r') as file:
    yaml_data = yaml.safe_load(file)


# Initialize a graph
g = Graph()

# Define your namespace
n = Namespace("http://example.org/taxonomies/abuses/")

# Add the taxonomy to the graph
scheme = yaml_data['scheme']
g.add((n[scheme['id']], RDF.type, SKOS.ConceptScheme))
g.add((n[scheme['id']], SKOS.prefLabel, Literal(scheme['title'])))
g.add((n[scheme['id']], SKOS.definition, Literal(scheme['description'])))

# Add concepts to the graph
for concept_key in yaml_data:
    if concept_key not in ['scheme']:
        concept = yaml_data[concept_key]
        concept_uri = n[concept['id']]
        g.add((concept_uri, RDF.type, SKOS.Concept))
        g.add((concept_uri, SKOS.prefLabel, Literal(concept['prefLabel'])))
        g.add((concept_uri, SKOS.definition, Literal(concept['description'])))
        if 'seeAlso' in concept:
            g.add((concept_uri, SKOS.seeAlso, URIRef(concept['seeAlso'])))

# Serialize the graph in Turtle format
g.serialize(destination='output.ttl', format='turtle')
