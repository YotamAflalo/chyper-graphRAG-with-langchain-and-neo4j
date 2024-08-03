PATH = 'books'

import getpass
import os
import json
import glob

from langchain_community.graphs import Neo4jGraph

from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from graph import driver
from config import ALLOWED_NODES, ALLOWED_RELETIONSHIPS, RELETIONSHIPS_PROPERTIES, NODES_PROPERTIES
from langchain_core.documents import Document
from PyPDF2 import PdfReader
gpt4o = ChatOpenAI(temperature=0, model_name="gpt-4o")

from llm import OpenAIEmbedding
llm_embedder = OpenAIEmbedding(model = 'text-embedding-3-small')
def dump_graph(graph_documents_props,driver:Neo4jGraph):
    
    # Store to neo4j
    driver.add_graph_documents(
    graph_documents_props, 
    baseEntityLabel=True, 
    include_source=True)

def full_book_constraction(path,starting_page=0,ending_page=None):
    '''
    This function reads a PDF file and constructs a single string containing the text from the specified page range.
    Parameters:
        path (str): The file path to the PDF.
        starting_page (int): The page number to start reading from. Default is 0.
        ending_page (int): The page number to stop reading at. If None, reads until the end of the document.
    Returns:
        str: The concatenated text from the specified pages of the PDF.
    '''
    book = PdfReader(path)
    if not ending_page: ending_page = len(book)
    full_book = ''
    for i in range(starting_page,ending_page): #len(book.pages) #i cuted the starting pages and the notes in the end
            page = book.pages[i].extract_text().replace('\t',' ').replace('https://www.8freebooks.net',' ')
            full_book = full_book + page + ' '
    return full_book

from langchain.text_splitter import RecursiveCharacterTextSplitter
def documents_constractor(full_book):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
        #separators=["\n\n", "\n", " ", ""]
    )
    docs = [Document(doc) for doc in text_splitter.split_text(full_book)]
    print(type(docs[0]))
    return docs
text = full_book_constraction(path="books/How_Not_to_Die.pdf") #,starting_page=10,ending_page=200) 
documents = documents_constractor(text)

def generate_prompt(doc_content):
    prompt_template = """
    Generate nodes and relationships for the following document:
    node instractions:
        1. wnen creating food nodes try to be as mach as spesific as you can.  try to use spesific fruit/vegtable/spise names. if you see a food "group" - make node for it too (one for the spesific food and one for the group),
        and connect to it all the nodes that are in his category.
        2. find all the node that apper at the text and part of the allowed_nodes.
        3. in 'meaning' Explain in simple words what the term in the name of the node is.
    relationships instractions:
        1. use CONTAINS for 'food' and 'nutritional value','microbiological component', where node(food) -[CONTAINS]->node('nutritional value'or 'microbiological component' or 'food')
        2. use ARE_KIND_OF for food that are part of food groups or disease that are part of disease group.
        3. use CAN_LEAD_TO or CAN_PREVENT for node(food,physical activity, nutritional supplement,nutritional value,microbiological component, drug, medical procedure) that can LEAD TO or CAN PREVENT node(disease)
        4. if spesific food have connection CAN_LEAD_TO or CAN_PREVENT with some target node,
        and the effect_mechanism refer to a nutritional value or microbiological component that exist in the food - make relationship between the nutritional value or microbiological component
        with the target node too.
    relationship_properties instractions:
        1. In Grounding_text you must give snipet from the context text you used to determine the relationship.
        2. In effect_mechanism you must explain how node1 affects node2, for example how a certain food affects the chance of getting a certain disease.
        3. In the Life extension/shortening period, you must first indicate whether it causes the extension/shortening of life
        (in one word, extension or shortening), then explain by how much.
    Document:
    {doc_content}

    Allowed nodes: {allowed_nodes}
    Allowed relationships: {allowed_relationships}
    Relationship properties: {relationship_properties}
    Node properties: {node_properties}

    """
    return prompt_template.format(
        doc_content=doc_content,
        allowed_nodes=','.join(ALLOWED_NODES),
        allowed_relationships=','.join(ALLOWED_RELETIONSHIPS),
        relationship_properties=','.join(RELETIONSHIPS_PROPERTIES),
        node_properties=','.join(NODES_PROPERTIES)
    )



i = 1


graph_dict = {}
pdf_files = glob.glob(os.path.join(PATH, "*.pdf"))
documents_dict ={}
for path in pdf_files:
    print(path)
    text = full_book_constraction(path=path,starting_page=300, ending_page=320)
    documents = documents_constractor(text)
    documents_dict[path] = documents
    
for doc_name, documents in documents_dict.items():
    for doc in documents: #my run stop after Processing Document 145
        # Create a callable prompt
        prompt_callable = lambda doc_content=doc.page_content: generate_prompt(doc_content)
        llm_transformer_props = LLMGraphTransformer(
            llm=gpt4o,
            allowed_nodes=ALLOWED_NODES,
            allowed_relationships=ALLOWED_RELETIONSHIPS,
            relationship_properties=RELETIONSHIPS_PROPERTIES,
            node_properties=NODES_PROPERTIES,
            
            prompt=prompt_callable  # Pass the callable prompt
        )

        graph_documents_props = llm_transformer_props.convert_to_graph_documents([doc])
        graph_documents_props[0].source.metadata['embedding'] = llm_embedder(doc.page_content)
        graph_documents_props[0].source.metadata['chank_number'] = i
        graph_documents_props[0].source.metadata['doc_name'] = doc_name

        graph_dict[i] =graph_documents_props[0].dict()
        print(f"Processing Document {i}")
        #print(doc.page_content[:100])  # Print the first 100 characters of the document content
        print('....................................................................................')

        print(f"Nodes: {graph_documents_props[0].nodes}")
        print('....................................................................................')
        print(f"Relationships: {graph_documents_props[0].relationships}")
        print('....................................................................................')
        dump_graph(graph_documents_props, driver)
        print('Graph dumped')
        if i%10==0: #for insurense 
            with open('graph_dict.json', 'w', encoding='utf-8') as f: 
                json.dump(graph_dict, f, ensure_ascii=False, indent=4)
        
        i += 1
        print('....................................................................................')

with open('graph_dict.json', 'w', encoding='utf-8') as f:
            json.dump(graph_dict, f, ensure_ascii=False, indent=4)

