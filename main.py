import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from utils.langchain_openrouter import ChatOpenRouter

load_dotenv()

MODEL_NAME:str = os.environ.get("MODEL_NAME")


llm = ChatOpenRouter(model_name=MODEL_NAME)
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic} in persion")
openrouter_chain = prompt | llm
try:
    for chunk in openrouter_chain.stream({"topic": "banana"}):
        print(chunk.content, end="", flush=True)
except ValueError as connection_error:
    print(f"can not resolve, because of connection error {ValueError}")