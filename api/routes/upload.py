from fastapi import APIRouter, UploadFile, File, Form
from utils.functions import upload_pdf, load_pdf, split_text
from utils.vectorstore import index_documents
from utils.functions import PDF_DIRECTORY
from ..schemas.common import ApiResponse

router = APIRouter()

@router.post("/chat/upload", response_model=ApiResponse)
async def upload_pdf_endpoint(
    user_id: str = Form(...),
    chat_id: str = Form(...),
    file: UploadFile = File(...)
):
    upload_pdf(file)
    file_path = PDF_DIRECTORY + file.filename
    docs = load_pdf(file_path)
    chunks = split_text(docs)
    index_documents(chunks, user_id, chat_id)
    return ApiResponse(message="PDF uploaded and indexed")