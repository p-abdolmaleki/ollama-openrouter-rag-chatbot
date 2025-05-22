import os
from dotenv import load_dotenv

from langchain_ollama import OllamaEmbeddings, ChatOllama
from utils.langchain_openrouter import ChatOpenRouter

load_dotenv()

def get_embedding_model():
    backend = os.environ.get("EMBEDDING_BACKEND")
    if backend == "ollama":
        return OllamaEmbeddings(model=os.environ.get("OLLAMA_EMBEDDING_MODEL"), base_url=os.environ.get("OLLAMA_BASE_URL"))
    else:
        raise ValueError(f"Unsupported EMBEDDING_BACKEND: {backend}")

def get_llm_model():
    backend = os.environ.get("LLM_BACKEND")
    if backend == "ollama":
        return ChatOllama(model=os.environ.get("OLLAMA_LLM_MODEL"), base_url=os.environ.get("OLLAMA_BASE_URL"))
    elif backend == "openrouter":
        return ChatOpenRouter(model_name=os.environ.get("OPENROUTER_LLM_MODEL"), api_key=os.environ.get("OPENROUTER_API_KEY"))
    else:
        raise ValueError(f"Unsupported LLM_BACKEND: {backend}")
