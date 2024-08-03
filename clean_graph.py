from graph import driver
from config import DELETE_QUERIES
# DELETE_QUERIES = [
#         "MATCH (:Food)-[r:CAN_PREVENT]->(:Food) DELETE r",
#         "MATCH (:Food)-[r:CAN_PREVENT]->(n:`Body organ`) DELETE r",
#         "MATCH (:Food)-[r:CONTAINS]->(:Body organ) DELETE r",
#         "MATCH (:Physical activity)-[r:CONTAINS]->(:Microbiological component) DELETE r",
#         "MATCH (:Food)-[r:CAN_PREVENT]->(:Micro organisem) DELETE r"
#     ]

def delete_connections(driver,delete_queries:list=[]):

    if len(delete_connections):
        i=0
        broken_queries = []
        with driver.session() as session:
            for query in delete_queries:
                try:
                    session.run(query)
                    i+=1
                except:
                    broken_queries.append(query)
        print("deleted {i} connections type")
        return broken_queries
    
delete_wrong_connecctions = delete_connections(driver=driver,delete_queries=DELETE_QUERIES)
print(delete_wrong_connecctions)

