#tool for chyper sherch
import sys
import os

# adding paths for easy lmport
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm import chat_model
from graph import driver
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about health and diet recommendations.
Convert the user's question based on the schema.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Do not return entire nodes or embedding properties.

Fine Tuning:

[]
Example Cypher Statements:

1. To find all the thing that can lead to some Disease:
```
MATCH (n)--[r:CAN_LEAD_TO]->(:Disease {{id:'disease name'}}))
RETURN n.id, r.effect_mechanism
```

2. To find all the thing that can prevent to some Disease:
```
MATCH (n)--[r:CAN_PREVENT]->(:Disease {{id:'disease name'}}))
RETURN n.id, r.effect_mechanism
```

3. find foods that have the same affact of some drug:
```
MATCH (d:Drug {{id:'Drug name'}})--[r:CAN_PREVENT]->(:Disease)<-[r2:CAN_PREVENT]--(n)
return n.id, r2.effect_mechanism )
```

Schema:
{schema}

Question:
{question}
"""
cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)
cypher_qa = GraphCypherQAChain.from_llm(
    cypher_llm=chat_model,
    graph=driver,
    verbose=True,
    cypher_prompt=cypher_prompt,
    llm=chat_model
)

## example:
#answer = cypher_qa(question="find all the disease that broccoli can prevent")
#print(answer)