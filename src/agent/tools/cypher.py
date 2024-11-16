#tool for chyper sherch
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
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about health and diet recommendations.
Convert the user's question based on the schema.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

instractions:
- ***all the id's starts with capital leter (like "Plant-Based Diet", or "Turmeric")
- if you reffering to type with more then one word in his name, use `type name`, for example: (nv:`Nutritional value`)
- try not to over complicat things
- If you need to pass the result of the aggregation function of another aggregation function, do it through the WITH

Example Cypher Statements:
1. To find all the thing that can lead to some Disease:
```
MATCH (n)--[r:CAN_LEAD_TO]->(:Disease {{id:'disease name'}}))
RETURN n, r;
```

2. To find all the thing that can prevent to some Disease:
```
MATCH (n)--[r:CAN_PREVENT]->(:Disease {{id:'disease name'}}))
RETURN n, r;
```

3. find foods that have the same affact of some drug:
```
MATCH (d:Drug {{id:'Drug name'}})-[r:CAN_PREVENT]->(:Disease)<-[r2:CAN_PREVENT]--(n)
return n, r2 )
```
4. find all the health benefits of some food:
```
MATCH (n:Food {{id:'Food name'}})-[r:CAN_PREVENT|CAN_REDUCE]->(d)

RETURN n,d, r;
```
Schema:
{schema}

Question:
{question}
"""
cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE) #לוודא איפה נכנסת הסמכה והשאלה
cypher_qa = GraphCypherQAChain.from_llm(  #rerun_CypherQAChain still dont work as well
    cypher_llm=chyper_model,
    graph=driver,
    verbose=True,
    cypher_prompt=cypher_prompt,
    llm=chat_model,
    # validate_cypher=True
)
####אני צריך להוסיף פה בדיקה, אם זה עובד - נהדר, אם לא - שיעשה ניסוי חוזר

## example:
#answer = cypher_qa(question="find all the disease that broccoli can prevent")
#print(answer)