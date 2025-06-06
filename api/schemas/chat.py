from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    question: str

class GenerateNameRequest(BaseModel):
    first_message: str
    answer_text: str
    chat_id: str
    user_id: str