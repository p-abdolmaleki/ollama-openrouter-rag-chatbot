import os
from dotenv import load_dotenv

from langchain_ollama import OllamaEmbeddings, ChatOllama
from utils.langchain_openrouter import ChatOpenRouter
from langchain_core.utils.utils import secret_from_env

load_dotenv()

def get_embedding_model():
    backend = os.environ.get("EMBEDDING_BACKEND")
    if backend == "ollama":
        return OllamaEmbeddings(model=os.environ.get("OLLAMA_EMBEDDING_MODEL")) #, base_url=os.environ.get("OLLAMA_EMBEDDING_BASE_URL"))
    else:
        raise ValueError(f"Unsupported EMBEDDING_BACKEND: {backend}")

def get_llm_model():
    backend = os.environ.get("LLM_BACKEND")
    if backend == "ollama":
        return ChatOllama(model=os.environ.get("OLLAMA_LLM_MODEL")) #, base_url=os.environ.get("OLLAMA_LLM_BASE_URL"))
    elif backend == "openrouter":
        return ChatOpenRouter(model_name=os.environ.get("OPENROUTER_LLM_MODEL"), api_key=os.environ.get("OPENROUTER_API_KEY"))
    else:
        raise ValueError(f"Unsupported LLM_BACKEND: {backend}")

def get_mongo_config():
    mongo_uri = os.environ.get("MONGO_URI")
    mongo_user = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
    mongo_pass = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
    mongo_db_name = os.environ.get("MONGO_INITDB_DATABASE")

    if not all([mongo_uri, mongo_user, mongo_pass, mongo_db_name]):
        raise ValueError("Missing MongoDB configuration in environment variables.")

    return {
        "uri": mongo_uri,
        "user": mongo_user,
        "password": mongo_pass,
        "db_name": mongo_db_name
    }