from fastapi import APIRouter
from ..schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse, ChatSessionResponse, GenerateNameRequest
from ..schemas.common import ApiResponse
from utils.chat_history import get_user_history, get_chat_sessions, save_chat, clear_user_history, update_chat_name
from utils.get_config import get_llm_model
from utils.vectorstore import retrieve_docs, clear_vectorstore
from utils.functions import answer_question, get_chat_name, get_usefull_chat_history
import uuid

router = APIRouter()

@router.get("/chats", response_model=ApiResponse)
def list_chats(user_id: str):
    sessions = get_chat_sessions(user_id)
    return ApiResponse(data=sessions)

@router.get("/history", response_model=ApiResponse)
def chat_history(user_id: str, chat_id: str):
    history = get_user_history(user_id, chat_id)
    return ApiResponse(data={"history": history})

@router.post("/start", response_model=ApiResponse)
def start_chat(user_id: str):
    chat_id = str(uuid.uuid4())[:8]
    sessions = get_chat_sessions(user_id)
    new_name = f"New Chat {len(sessions)+1}"
    save_chat(user_id, chat_id, chat_name=new_name, message=None)
    return ApiResponse(data={"chat_id": chat_id, "chat_name": new_name})

@router.post("/ask", response_model=ApiResponse)
def chat_message(request: ChatRequest):
    docs = retrieve_docs(request.question, request.user_id, request.chat_id)
    model = get_llm_model()
    history = get_user_history(request.user_id, request.chat_id)
    usefull_chat_history_resp = get_usefull_chat_history(request.question, history, model)
    usefull_chat_history_text = usefull_chat_history_resp.content if hasattr(usefull_chat_history_resp, 'content') else str(usefull_chat_history_resp)
    answer_obj = answer_question(request.question, docs, usefull_chat_history_text, model)
    answer_val = answer_obj['answer']
    answer_text = answer_val.content if hasattr(answer_val, 'content') else answer_val
    save_chat(request.user_id, request.chat_id, message=request.question, answer=answer_text)
    return ApiResponse(data={"answer": answer_text})

@router.post("/clear_history", response_model=ApiResponse)
def clear_history(user_id: str, chat_id: str):
    clear_user_history(user_id, chat_id)
    return ApiResponse(message="Chat history cleared")

@router.post("/delete_files", response_model=ApiResponse)
def delete_files(user_id: str, chat_id: str):
    clear_vectorstore(user_id, chat_id)
    return ApiResponse(message="Files and vectors deleted")

@router.post("/generate_name", response_model=ApiResponse)
def generate_chat_name(request: GenerateNameRequest):
    model = get_llm_model()
    name_resp = get_chat_name(request.first_message, request.answer_text, model)
    new_label = name_resp.content.strip() if hasattr(name_resp, 'content') else str(name_resp).strip()
    update_chat_name(request.user_id, request.chat_id, new_label)
    return ApiResponse(data={"chat_name": new_label})

@router.post("/useful_history", response_model=ApiResponse)
def useful_history(question: str, user_id: str, chat_id: str):
    model = get_llm_model()
    history = get_user_history(user_id, chat_id)
    usefull_chat_history_resp = get_usefull_chat_history(question, history, model)
    usefull_chat_history_text = usefull_chat_history_resp.content if hasattr(usefull_chat_history_resp, 'content') else str(usefull_chat_history_resp)
    return ApiResponse(data={"useful_history": usefull_chat_history_text})