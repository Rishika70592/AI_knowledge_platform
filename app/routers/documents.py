from fastapi import APIRouter, Depends, UploadFile, File
from app.services.ingestion import ingest_document
from app.core.dependencies import get_current_user
from app.models import User

router = APIRouter()

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    contents = await file.read()
    
    result = await ingest_document(filename=file.filename, file_bytes=contents, user_id=current_user.id)
    return {"document_id": str(result.id), "status": result.status, "chunks_created": result.chunk_count}