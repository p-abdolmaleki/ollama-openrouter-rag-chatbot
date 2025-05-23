from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

PDF_DIRECTORY = "pdfs/"

base_template = """
You are an assistant who answers questions using only the provided context and chat history. Follow these rules:

- If the answer is found directly in the context, answer based only on the context and clearly state that your answer is based on the provided context.
- If the answer is not in the context but is in the chat history, answer based on the chat history and clearly state that your answer is based on the previous conversation.
- If the answer is found in both the context and the chat history, use both sources and clearly state that your answer is based on the context and previous conversation.
- If the answer is not found in either the context or the chat history, respond using your own internal knowledge and clearly state that the answer is based on your own internal knowledge.

Context:
{context}

Chat History:
{history}

Question:
{question}

Answer:
"""

chat_name_template = """
Please give a suitable name for this conversation. Only return the name.

Question: 
{question}
Answer: 
{answer_text}
Chat Name:
"""

usefull_chat_history_template = """
You are an assistant tasked with identifying all parts of a conversation that are relevant to a specific user question.

Instructions:
- Read the entire chat history and the given user question.
- Return only the parts of the chat history that are relevant to answering the question.
- Do not summarize or explain. Just extract and return the original text from the chat history that relates to the question.
- If nothing is relevant, return nothing.

Chat History:
{chat_history}

Question:
{question}

Relevant parts:
"""

def upload_pdf(file):
    with open(PDF_DIRECTORY + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()

def split_text(documents, chunk_size=300, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        source = chunk.metadata.get("source", "Unknown source")
        page = chunk.metadata.get("page", "Unknown page")
        chunk.metadata["source"] = source
        chunk.metadata["page"] = page

    return chunks

def answer_question(question, retrieved_docs, user_history, model, config=None):
    context = ""
    sources = set()
    for doc in retrieved_docs:
        context += doc.page_content + "\n\n"
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", "Unknown page")
        sources.add(f"{source.replace(PDF_DIRECTORY, '')} (Page {page})")

    prompt = ChatPromptTemplate.from_template(base_template)
    chain = prompt | model
    answer = chain.invoke({"question": question, "context": context, "history": user_history}, config=config)

    return {
        "answer": answer,
        "sources": list(sources)
    }

def get_chat_name(question, answer_text, model):
    prompt = ChatPromptTemplate.from_template(chat_name_template)
    chain = prompt | model
    name = chain.invoke({"question": question, "answer_text": answer_text})
    return name

def get_usefull_chat_history(history, question, model):
    prompt = ChatPromptTemplate.from_template(usefull_chat_history_template)
    chain = prompt | model
    summary = chain.invoke({"chat_history": history, "question": question})
    return summary
