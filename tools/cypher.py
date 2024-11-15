#tool for chyper sherch
import sys
import os

# adding paths for easy lmport
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm import chat_model,chyper_model
from graph import driver
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from langchain.prompts.prompt import PromptTemplate
from langchain.chains.base import Chain

class rerun_CypherQAChain(GraphCypherQAChain):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _call(self, inputs):
        try:
            return super()._call(inputs)
        except Exception as e:
            # Get the original question, schema, and Cypher query
            question = inputs.get("input", "")
            schema = inputs.get("schema", "")
            chat_history = inputs.get("chat_history", "")
            cypher_query = self.cypher_prompt.format_prompt({"question": question, "schema": schema}).to_string()

            # Use the LLM to generate a fixed Cypher query
            prompt = f"The original Cypher query was: {cypher_query}\nHere is the error: {e}\nPlease provide a corrected Cypher query based on the schema: {schema}\nPrevious conversation history: {chat_history}"
            fixed_cypher_query = self.llm(prompt)

            # Send the fixed Cypher query to the graph driver
            result = self.graph.run(fixed_cypher_query)
            return {"output": result}

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about health and diet recommendations.
Convert the user's question based on the schema.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Do not return entire nodes or embedding properties.

Fine Tuning:
- make shure to use correct Cypher. 
- if you reffering to type with more then one word in his name, use `type name`, for example: (nutrient:`Nutritional value`)
- try not to over complicat things
- case sensitivity: note that names may start with an upper/lowercase letter, and appear in the singular/plural. 
 Search in a way that includes all the options (e.g. cancer or Cancer or cancers).
- If you need to pass the result of the aggregation function of another aggregation function, do it through the WITH

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
4. find all the health benefits of some food:
```
MATCH (n:Food {{id:'Food name'}})--[r:CAN_PREVENT|CAN_REDUCE]->(d)

RETURN d.id, r.effect_mechanism
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
    validate_cypher=True
)
####אני צריך להוסיף פה בדיקה, אם זה עובד - נהדר, אם לא - שיעשה ניסוי חוזר

## example:
#answer = cypher_qa(question="find all the disease that broccoli can prevent")
#print(answer)