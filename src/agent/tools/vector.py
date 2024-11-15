#tools for vector sherch - embeddig
import os

# adding paths for easy lmport
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)
from src.llm import chat_model,langchain_embeddings
from src.graph import driver

from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate


neo4jvector = Neo4jVector.from_existing_index(
    langchain_embeddings,                          
    graph=driver,                           
    index_name="doc_embedding",      
    node_label="Document",   
    text_node_property="text",       
    embedding_node_property="embedding", 
    retrieval_query="""
RETURN
    node.text AS text,
    score,
    {
        doc_id: node.chank_number,
        MENTIONS: [ (node)-[:MENTIONS]->(entity) | [entity.id,entity.meaning] ]
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()

instructions = (
    "Use the given context to answer the question."
    "If you don't know the answer, say you don't know."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chat_model, prompt)
text_retriever = create_retrieval_chain(
    retriever, 
    question_answer_chain
)

def get_doc_text(input):
    return text_retriever.invoke({"input": input})

## example:
#answer = get_doc_text("tell me about the affect of broccoli")
#print(answer)
