import streamlit as st
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from utils.functions import upload_pdf, load_pdf, split_text, answer_question, PDF_DIRECTORY
from utils.vectorstore import index_documents, retrieve_docs, clear_vectorstore
from utils.chat_history import save_chat, get_user_history, clear_user_history, get_chat_sessions, update_chat_name
from utils.model_config import get_llm_model
import uuid

model = get_llm_model()
st.title("RAG Chatbot")

# User login
if "user_id" not in st.session_state or st.session_state.user_id is None:
    username = st.text_input("Enter your username:")
    if st.button("Login") and username:
        st.session_state.user_id = username
        try:
            st.rerun()
        except AttributeError:
            pass

if "user_id" in st.session_state and st.session_state.user_id:
    user_id = st.session_state.user_id
    st.success(f"Welcome {user_id}!")
    if st.button('Logout'):
        st.session_state.user_id = None
        try:
            st.rerun()
        except AttributeError:
            pass

    # Chat session management
    sessions = get_chat_sessions(user_id)
    if not sessions:
        default_id = str(uuid.uuid4())[:8]
        save_chat(user_id, default_id, chat_name="New Chat 1", message=None, answer=None, sources=[])
        sessions = get_chat_sessions(user_id)

    labels = [s['chat_name'] or s['chat_id'] for s in sessions]
    chat_map = {s['chat_name'] or s['chat_id']: s['chat_id'] for s in sessions}

    selected_label = st.selectbox(
        "Select a chat:",
        labels,
        index=labels.index(st.session_state.get('chat_label', labels[0]))
            if st.session_state.get('chat_label') in labels else 0
    )
    chat_id = chat_map[selected_label]
    st.session_state.chat_id = chat_id
    st.session_state.chat_label = selected_label

    # Initialize set of uploaded files per chat
    uploaded_key = f"uploaded_{user_id}_{chat_id}"
    if uploaded_key not in st.session_state:
        st.session_state[uploaded_key] = set()

    # New chat button
    if st.button("➕ Start New Chat"):
        new_id = str(uuid.uuid4())[:8]
        new_name = f"New Chat {len(sessions)+1}"
        save_chat(user_id, new_id, chat_name=new_name, message=None, answer=None, sources=[])
        sessions = get_chat_sessions(user_id)
        st.success(f"Started new chat: {new_name}")
        try:
            st.rerun()
        except AttributeError:
            pass

    st.write(f"🗂️ Current Chat: **{st.session_state.chat_label}** (`{chat_id}`)")

    # Utilities
    if st.button("🗑️ Delete your uploaded files & vectors in this chat"):
        clear_vectorstore(user_id, chat_id)
        st.session_state[uploaded_key].clear()
        st.success("All your uploaded files have been deleted.")
    if st.button("🗑️ Delete chat history"):
        clear_user_history(user_id, chat_id)
        st.success("Your chat history has been deleted.")

            # PDF upload and indexing only new files
    uploader_widget_key = f"uploader_{user_id}_{chat_id}"
    uploaded_files = st.file_uploader(
        "Upload PDF", type=["pdf"], accept_multiple_files=True, key=uploader_widget_key
    )
    if uploaded_files:
        for f in uploaded_files:
            if f.name not in st.session_state[uploaded_key]:
                upload_pdf(f)
                docs = load_pdf(PDF_DIRECTORY + f.name)
                chunks = split_text(docs)
                index_documents(chunks, user_id, chat_id)
                st.session_state[uploaded_key].add(f.name)
        st.success("All new PDFs processed and indexed.")

    # Display history"
    history = get_user_history(user_id, chat_id)
    if history:
        for item in history:
            if item.get('message'):
                st.chat_message("user").write(item['message'])
            if item.get('answer'):
                st.chat_message("assistant").write(item['answer'])
                if item.get('sources'):
                    with st.chat_message("assistant"):
                        with st.expander("📚 منابع"):
                            for src in item['sources']:
                                st.markdown(f"- {src}")

    # User question
    question = st.chat_input("Ask your question:")
    if question:
        st.chat_message("user").write(question)
        handler = StreamlitCallbackHandler(st.empty())
        docs = retrieve_docs(question, user_id=user_id, chat_id=chat_id)
        answer_obj = answer_question(
            question, docs, history, model,
            config={"callbacks": [handler]}
        )
        answer_val = answer_obj['answer']
        answer_text = answer_val.content if hasattr(answer_val, 'content') else answer_val
        sources = answer_obj['sources']
        st.chat_message("assistant").write(answer_text)
        if sources:
            with st.chat_message("assistant"):
                with st.expander("📚 منابع"):
                    for src in sources:
                        st.markdown(f"- {src}")
        # Rename chat on first question
        if st.session_state.chat_label.startswith("New Chat"):
            prompt = (
                "Please give me a suitable name for this conversation. Only return the name."
                f"Question: {question}\nAnswer: {answer_text}"
            )
            name_resp = model.invoke(prompt)
            new_label = name_resp.content.strip() if hasattr(name_resp, 'content') else str(name_resp).strip()
            st.session_state.chat_label = new_label
            update_chat_name(user_id, chat_id, new_label)
            save_chat(
                user_id, chat_id,
                chat_name=st.session_state.chat_label,
                message=question, answer=answer_text, sources=sources
            )
            st.success(f"Conversation renamed to: {new_label}")
            try:
                st.rerun()
            except AttributeError:
                pass
        else:
            save_chat(
                user_id, chat_id,
                chat_name=st.session_state.chat_label,
                message=question, answer=answer_text, sources=sources
            )
