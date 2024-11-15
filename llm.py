
from openai import OpenAI
import os
class my_OpenAIEmbedding:
    def __init__(self,model = "text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=self.model).data[0].embedding
from langchain_openai import OpenAIEmbeddings

langchain_embeddings = OpenAIEmbeddings(model="text-embedding-3-small") #for the vector tool


# how to use
# embedding_instance = OpenAIEmbedding(model="text-embedding-3-small")
# embedding = embedding_instance.get_embedding("Your text here")
# print(embedding[:20])

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from llm_config import anthropic_chat_model, anthropic_cypher_model
chat_model = ChatAnthropic(
    model=anthropic_chat_model,
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    api_key= os.getenv('CLAUDE_KEY')
)

chyper_model = ChatAnthropic(
    model=anthropic_cypher_model,
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    api_key= os.getenv('CLAUDE_KEY')
)

gpt4o = ChatOpenAI(temperature=0, model_name="gpt-4o")
