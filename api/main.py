from fastapi import FastAPI
from .routes import auth, chat, upload

app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG Chatbot (login, chat, upload)",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])