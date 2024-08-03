DELETE_QUERIES = [
        "MATCH (:Food)-[r:CAN_PREVENT]->(:Food) DELETE r",
        "MATCH (:Food)-[r:CAN_PREVENT]->(n:`Body organ`) DELETE r",
        "MATCH (:Food)-[r:CONTAINS]->(:Body organ) DELETE r",
        "MATCH (:Physical activity)-[r:CONTAINS]->(:Microbiological component) DELETE r",
        "MATCH (:Food)-[r:CAN_PREVENT]->(:Micro organisem) DELETE r"
    ]

ALLOWED_NODES =['food', 'nutritional supplement','nutritional value','microbiological component', 'drug', 'medical procedure',
                                'body organ', 'disease', 'physical activity','micro organisem']
ALLOWED_RELETIONSHIPS =['CONTAINS', 'ARE_KIND_OF','CAN_LEAD_TO', 'CAN_PREVENT','CAN_REDUCE','REQUIRED_FOR']
RELETIONSHIPS_PROPERTIES =['Grounding_text','effect_mechanism','cost','The_intensity_of_the_effect','Life extension/shortening period']
NODES_PROPERTIES = ['amount_required','group','cost','amount']