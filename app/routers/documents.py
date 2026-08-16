from fastapi import APIRouter, UploadFile, File
from app.services.ingestion import ingest_document

router = APIRouter()

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    result = await ingest_document(filename=file.filename, file_bytes=contents)
    return {"document_id": str(result.id), "status": result.status, "chunks_created": result.chunk_count}