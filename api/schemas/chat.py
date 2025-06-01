from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str

class ChatHistoryItem(BaseModel):
    message: str
    answer: str
    sources: Optional[list] = []

class ChatHistoryResponse(BaseModel):
    history: List[ChatHistoryItem]

class ChatSessionResponse(BaseModel):
    chat_id: str
    chat_name: str

class GenerateNameRequest(BaseModel):
    first_message: str
    answer_text: str
    chat_id: str
    user_id: str