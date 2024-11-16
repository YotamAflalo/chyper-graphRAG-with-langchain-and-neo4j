#tool for docs chyper sherch
import os
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)
# adding paths for easy lmport
from src.llm import chat_model,chyper_model
from src.graph import driver
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from langchain.prompts.prompt import PromptTemplate
from langchain.chains.base import Chain


CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to pull relevant document from the db.

Identify which entities the user is asking about, 
then formulate a cypher query that will pull the text of all documents that mention those concepts.

For example, if the user asks about lung cancer, you will pull all node documents that mention lung cancer

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

instractions:
- Do not return the embedding properties.
- all the id's starts with capital leter (like "Plant-Based Diet", or "Turmeric")
- if you reffering to type with more then one word in his name, use `type name`, for example: (nv:`Nutritional value`)
- If you need to pass the result of the aggregation function of another aggregation function, do it through the WITH

Example Cypher Statements:
1. user: find all the documents that mention Cancer:
answer:
```
MATCH (d:Document)-[:MENTIONS]->(n:Disease {id:'Cancer'})
RETURN n, d.chank_number,d.text;
```

2. user: find all the documents that talk about ways to prevent Cancer:
```
MATCH (d:Document)-[:MENTIONS]->(n:Disease {id:'Cancer'})<-[t:CAN_PREVENT]-(r)<-[:MENTIONS]-(d)
RETURN n, d.chank_number,d.text,r,t;```

3. user: find all the documents that talk about drugs for Cancer:
```
MATCH (d:Document)-[:MENTIONS]->(n:Drug)-[:CAN_PREVENT]->(:Disease {id:'Cancer'})
return d.chank_number,d.text;
```

Schema:
{schema}

Question:
{input}
"""
cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE) #לוודא איפה נכנסת הסמכה והשאלה
cypher_hybrid = GraphCypherQAChain.from_llm(  #rerun_CypherQAChain still dont work as well
    cypher_llm=chyper_model,
    graph=driver,
    verbose=True,
    cypher_prompt=cypher_prompt,
    llm=chat_model,
)
