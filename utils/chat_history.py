from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

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

def save_chat(user_id, chat_id, chat_name=None, message=None, answer=None, sources=None):
    if hasattr(answer, 'content'):
        answer_text = answer.content
    elif answer is not None:
        answer_text = str(answer)
    else:
        answer_text = None
    if isinstance(sources, list):
        sources_list = sources
    else:
        sources_list = []

    collection.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "chat_name": chat_name,
        "message": message,
        "answer": answer_text,
        "sources": sources_list,
        "timestamp": datetime.utcnow()
    })

def get_user_history(user_id, chat_id):
    cursor = collection.find({"user_id": user_id, "chat_id": chat_id}).sort("timestamp", 1)
    return [
        {
            "message": doc["message"],
            "answer": doc["answer"],
            "sources": doc.get("sources", [])
        }
        for doc in cursor
    ]

def update_chat_name(user_id, chat_id, chat_name):
    collection.update_many({"user_id": user_id, "chat_id": chat_id}, {"$set": {"chat_name": chat_name}})

def clear_user_history(user_id, chat_id):
    collection.delete_many({"user_id": user_id, "chat_id": chat_id})

def get_chat_sessions(user_id):
    session_ids = collection.distinct("chat_id", {"user_id": user_id})
    sessions = []
    for sid in session_ids:
        doc = collection.find_one({"user_id": user_id, "chat_id": sid, "chat_name": {"$ne": None}})
        name = doc["chat_name"] if doc and doc.get("chat_name") else sid
        sessions.append({"chat_id": sid, "chat_name": name})
    return sessions
