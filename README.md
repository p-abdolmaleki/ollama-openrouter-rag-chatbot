# Ollama OpenRouter RAG Chatbot

A local chatbot powered by **Ollama** for embeddings and **OpenRouter** for LLM responses, wrapped in a **Streamlit** app.

## 🚀 How to Run

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
````

2. **Install [Ollama](https://ollama.com/download)** (follow the installation guide for your OS).

3. **Pull your preferred embedding model using Ollama:**

```bash
ollama pull <embedding_model_name>
```

(For example: `ollama pull deepseek-r1:1.5b`)

4. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

5. **Configure environment variables:**

* Copy the sample environment file:

```bash
cp sample.env .env
```

* Open `.env` and fill in your keys and models:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
LLM_MODEL_NAME=your_openrouter_model_name
EMBEDDING_MODEL_NAME=your_ollama_embedding_model_name
```

6. **Run the chatbot:**

```bash
streamlit run main.py
```

🎉 Done! Enjoy chatting with your local chatbot.

---


## 📚 Notes

* You'll need a valid API key from [OpenRouter](https://openrouter.ai/) to access LLMs.
* Make sure the embedding model specified in `.env` is already pulled via Ollama before running the app.


