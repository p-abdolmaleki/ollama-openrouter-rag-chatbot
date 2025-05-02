import os
import faiss
import shutil
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.in_memory import InMemoryDocstore


load_dotenv()

BASE_VECTOR_DB_DIR = "vector_db/"

EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME")
embedding = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)

def get_user_vectorstore_dir(user_id):
    return os.path.join(BASE_VECTOR_DB_DIR, user_id)

def get_index_file(user_id):
    return os.path.join(get_user_vectorstore_dir(user_id), "index.faiss")

def load_vectorstore(user_id):
    user_dir = get_user_vectorstore_dir(user_id)
    index_file = get_index_file(user_id)

    if os.path.exists(index_file):
        return FAISS.load_local(user_dir, embedding, allow_dangerous_deserialization=True)
    else:
        dim = len(embedding.embed_query("dummy"))
        index = faiss.IndexFlatL2(dim)
        return FAISS(embedding.embed_query, index, InMemoryDocstore({}), {})

def save_vectorstore(vector_store, user_id):
    user_dir = get_user_vectorstore_dir(user_id)
    vector_store.save_local(user_dir)

def index_documents(documents, user_id):
    vector_store = load_vectorstore(user_id)
    vector_store.add_documents(documents)
    save_vectorstore(vector_store, user_id)

def clear_vectorstore(user_id):
    user_dir = get_user_vectorstore_dir(user_id)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)

def retrieve_docs(query, user_id, k=7, fetch_k=20, strategy="mmr"):
    vector_store = load_vectorstore(user_id)

    if strategy == "mmr":
        return vector_store.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k)
    elif strategy == "top_k":
        return vector_store.similarity_search(query, k=k)
    elif strategy == "with_score":
        return vector_store.similarity_search_with_score(query, k=k)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
