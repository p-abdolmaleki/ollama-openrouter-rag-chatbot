from tinydb import TinyDB, Query


DB_FILE = "chat_history.json"
db = TinyDB(DB_FILE)

def save_chat(user_id, message, answer, sources):
    if hasattr(answer, 'content'):
        answer_text = answer.content
    else:
        answer_text = str(answer)
    if type(sources) == list:
        sources_list = sources
    else:
        sources_list = []

    db.insert({"user_id": user_id, "message": message, "answer": answer_text, "sources": sources_list})

def get_user_history(user_id):
    User = Query()
    return db.search(User.user_id == user_id)

def clear_user_history(user_id):
    User = Query()
    db.remove(User.user_id == user_id)