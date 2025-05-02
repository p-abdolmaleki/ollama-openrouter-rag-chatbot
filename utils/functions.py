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
    return splitter.split_documents(documents)

def answer_question(question, retrieved_docs, user_history, model, config=None):
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    history_str = "\n".join([f"User: {h['message']} | Assistant: {h['answer']}" for h in user_history])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context, "history": history_str}, config=config)
