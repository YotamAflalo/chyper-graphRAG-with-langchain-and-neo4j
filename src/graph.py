import os
from langchain_community.graphs import Neo4jGraph

driver = Neo4jGraph(
    url= os.getenv('NEO4J_URI'),
    password=os.getenv('NEO4J_PASSWORD'),
    username=os.getenv('NEO4J_USERNAME')
    )


