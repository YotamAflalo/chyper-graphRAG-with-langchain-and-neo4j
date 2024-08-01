
import os

from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

driver = Neo4jGraph(
    url= os.getenv('NEO4J_URI'),
    password=os.getenv('NEO4J_PASSWORD'),
    username=os.getenv('NEO4J_USERNAME')
    )

query = """
        CREATE VECTOR INDEX doc_embedding IF NOT EXISTS
        FOR (d:Document)
        ON d.embedding
        OPTIONS {indexConfig: {
            `vector.dimensions`: 1536,
            `vector.similarity_function`: 'cosine'}
        }
        """
driver.query(query)

