# Ollama OpenRouter RAG Chatbot

A local Retrieval-Augmented Generation (RAG) chatbot built with **Ollama**, **OpenRouter**, and **Streamlit**.  
It uses PDFs as knowledge sources and stores multi-chat history in **MongoDB**.

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/p-abdolmaleki/ollama-openrouter-rag-chatbot.git
cd ollama-openrouter-rag-chatbot
```

### 2. Install Ollama

Download and install from: [https://ollama.com/download](https://ollama.com/download)

### 3. Pull embedding model via Ollama

```bash
ollama pull <model_name>
```

You can replace `model_name` with your preferred embedding model (must match `.env`).

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy the sample config and edit it:

```bash
cp sample.env .env
```

Edit `.env` and provide:

* Your `OPENROUTER_API_KEY`
* LLM and embedding model names
* MongoDB connection settings

### 6. Start the app

```bash
streamlit run main.py
```

✅ You’re all set! Upload some PDFs and start chatting.

---

## ⚙️ Environment Configuration (`.env`)

| Variable                 | Description                          |
| ------------------------ | ------------------------------------ |
| `LLM_BACKEND`            | `openrouter` or `ollama`             |
| `EMBEDDING_BACKEND`      | Only `ollama` supported for now      |
| `OPENROUTER_API_KEY`     | Your OpenRouter API key              |
| `OPENROUTER_LLM_MODEL`   | OpenRouter model name (e.g. gpt-3.5) |
| `OLLAMA_LLM_MODEL`       | Ollama model name (e.g. mistral)     |
| `OLLAMA_EMBEDDING_MODEL` | Embedding model via Ollama           |
| `MONGO_URI`              | MongoDB URI (e.g. localhost:27017)   |
| `MONGO_INITDB_DATABASE`  | DB name for storing chats            |

---

## 🆕 API Endpoints

A FastAPI backend is now included for programmatic access.  
**Base URL:** `/api`

### Authentication

- `POST /api/auth/login`  
  Request: `{ "username": "your_name" }`  
  Response: `{ "user_id": "..." }`

### Chat

- `GET /api/chat/chats?user_id=...`  
  List chat sessions for a user.

- `POST /api/chat/start`  
  Start a new chat.  
  Request: `{ "user_id": "..." }`

- `POST /api/chat/ask`  
  Ask a question in a chat.  
  Request: `{ "user_id": "...", "chat_id": "...", "question": "..." }`

- `GET /api/chat/history?user_id=...&chat_id=...`  
  Get chat history.

- `POST /api/chat/clear_history`  
  Clear chat history.  
  Request: `{ "user_id": "...", "chat_id": "..." }`

- `POST /api/chat/delete_files`  
  Delete uploaded files and vectors for a chat.  
  Request: `{ "user_id": "...", "chat_id": "..." }`

- `POST /api/chat/generate_name`  
  Generate a chat name based on the first message and answer.  
  Request: `{ "first_message": "...", "answer_text": "...", "chat_id": "...", "user_id": "..." }`

- `POST /api/chat/useful_history`  
  Get useful chat history for a question.  
  Request: `{ "question": "...", "user_id": "...", "chat_id": "..." }`

### Upload

- `POST /api/upload/chat/upload`  
  Upload a PDF for a chat.  
  Form fields: `user_id`, `chat_id`, `file` (PDF)

---

## 📝 Features

* 📄 PDF uploader with chunked indexing
* 🧠 Local embeddings via Ollama
* 💬 OpenRouter or Ollama as LLM
* 🗂️ Multi-chat history stored in MongoDB
* 🔁 Persistent context and memory
* 🧪 Ready for further backend upgrades
* 🆕 RESTful API for chat, upload, and management

---

## 🧠 Notes

* Make sure the model is pulled via Ollama before running.
* OpenRouter requires a valid API key from [https://openrouter.ai](https://openrouter.ai).
