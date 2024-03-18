import spacy

# Load the pre-trained NER model
nlp = spacy.load("en_core_web_sm")

def extract_locations(text):
    # Process the text with spaCy
    doc = nlp(text)
    # Extract entities identified as GPE or LOC
    locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
    return locations

# Example usage
ship_from_text = "Ships from Australia Europe"
ship_to_text = "Ships to Worldwide"

ship_from_locations = extract_locations(ship_from_text)
ship_to_locations = extract_locations(ship_to_text)

# Now, you can add these locations to your RDF graph