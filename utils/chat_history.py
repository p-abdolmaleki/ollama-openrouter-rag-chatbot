from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DB_NAME = os.environ.get("MONGO_INITDB_DATABASE")

client = MongoClient(
    MONGO_URI,
    username=MONGO_USER,
    password=MONGO_PASS,
    authSource="admin"
)

db = client[MONGO_DB_NAME]
collection = db["chat_history"]

def save_chat(user_id, message, answer, sources):
    if hasattr(answer, 'content'):
        answer_text = answer.content
    else:
        answer_text = str(answer)
    if isinstance(sources, list):
        sources_list = sources
    else:
        sources_list = []
    db.chat_history.insert_one({
        "user_id": user_id,
        "message": message,
        "answer": answer_text,
        "sources": sources_list
    })

def get_user_history(user_id):
    cursor = db.chat_history.find({"user_id": user_id})
    return [{"message": doc["message"], "answer": doc["answer"], "sources": doc.get("sources", [])} for doc in cursor]

def clear_user_history(user_id):
    db.chat_history.delete_many({"user_id": user_id})
