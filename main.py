import os
from dotenv import load_dotenv
import streamlit as st
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from utils.langchain_openrouter import ChatOpenRouter
from utils.functions import upload_pdf, load_pdf, split_text, answer_question, PDF_DIRECTORY
from utils.vectorstore import index_documents, retrieve_docs, clear_vectorstore
from utils.chat_history import save_chat, get_user_history, clear_user_history

load_dotenv()

LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")
model = ChatOpenRouter(model_name=LLM_MODEL_NAME)

st.title("RAG Chatbot")

if "user_id" not in st.session_state:
    username_input = st.text_input("Enter your username:")
    if st.button("Login") and username_input:
        st.session_state.user_id = username_input

if "user_id" in st.session_state:
    st.success(f"Welcome {st.session_state.user_id}!")

    if st.button("🗑️ Delete all your uploaded files & vectors"):
        clear_vectorstore(st.session_state.user_id)
        st.success("All your uploaded files have been deleted.")
    
    if st.button("🗑️ Delete your chat history"):
        clear_user_history(st.session_state.user_id)
        st.success("Your chat history has been deleted.")

    upload_file = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True)

    if upload_file:
        for f in upload_file:
            upload_pdf(f)
            docs = load_pdf(PDF_DIRECTORY + f.name)
            chunks = split_text(docs)
            index_documents(chunks, st.session_state.user_id)
        st.success("All PDFs processed and indexed.")

    user_history = get_user_history(st.session_state.user_id)
    if user_history:
        st.write("Chat history:")
        for h in user_history:
            st.chat_message("user").write(h["message"])
            st.chat_message("assistant").write(h["answer"])

    question = st.chat_input("Ask your question:")
    if question:
        st.chat_message("user").write(question)

        stream_placeholder = st.empty()
        stream_handler = StreamlitCallbackHandler(stream_placeholder)

        retrieved_docs = retrieve_docs(question, user_id=st.session_state.user_id)

        answer_obj = answer_question(
            question,
            retrieved_docs,
            user_history,
            model,
            config={"callbacks": [stream_handler]}
        )

        answer_text = getattr(answer_obj["answer"], "content", str(answer_obj["answer"]))
        sources_list = answer_obj["sources"]
        sources_text = "\n".join(f"- {src}" for src in sources_list)

        save_chat(st.session_state.user_id, question, answer_text)

        st.chat_message("assistant").write(answer_text)
        if sources_list:
            with st.chat_message("assistant"):
                with st.expander("📚 منابع"):
                    for src in sources_list:
                        st.markdown(f"- {src}")
        # st.chat_message("assistant").write(f"{answer_text}\n\n📚 منابع:\n{sources_text}")
