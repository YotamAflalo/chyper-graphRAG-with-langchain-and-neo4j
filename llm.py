
from openai import OpenAI
import os
class OpenAIEmbedding:
    def __init__(self,model = "text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=self.model).data[0].embedding
from langchain_openai import OpenAIEmbeddings

langchain_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# how to use
# embedding_instance = OpenAIEmbedding(model="text-embedding-3-small")
# embedding = embedding_instance.get_embedding("Your text here")
# print(embedding[:20])

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

chat_model = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    api_key= os.getenv('CLAUDE_KEY')
)
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
# ai_msg = chat_model.invoke(messages)
# print(ai_msg)

gpt4o = ChatOpenAI(temperature=0, model_name="gpt-4o")
