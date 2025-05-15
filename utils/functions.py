from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

PDF_DIRECTORY = "pdfs/"

template = """
You are an assistant who answers questions based only on the text provided and the chat history.
Use the following guidelines:

- If the answer is found directly in the text, answer based only on the text and explicitly state that the answer is based on the text provided.
- If the answer is not found in the text but is in the chat history, answer based on the chat history and explicitly state that the answer is based on previous conversations.
- If the answer is found in a combination of text and chat history, answer based on the text and chat history and explicitly state that the answer is based on the text and previous conversations.
- If the answer is found neither in the text nor in the chat history, answer based on your own internal knowledge and explicitly state that the answer is based on your own internal knowledge.

Context:
{context}

Chat history:
{history}

Question:
{question}

Answer:
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

    history_str = "\n".join([f"User: {h['message']} | Assistant: {h['answer']}" for h in user_history])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    answer = chain.invoke({"question": question, "context": context, "history": history_str}, config=config)

    return {
        "answer": answer,
        "sources": list(sources)
    }