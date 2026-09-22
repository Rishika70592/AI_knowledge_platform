from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from app.core.dependencies import get_current_user
from app.models import User, ChatMessage, Document
from app.db.db import AsyncSessionLocal

router = APIRouter()


@router.get("/chat/history")
async def get_chat_history(limit: int = Query(50, le=200), current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == current_user.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return [
            {
                "id": str(m.id),
                "question": m.question,
                "answer": m.answer,
                "source_document_ids": m.source_document_ids,
                "created_at": m.created_at,
            }
            for m in reversed(messages)  # oldest -> newest
        ]


@router.get("/documents")
async def list_documents(current_user: User = Depends(get_current_user)):
    """
    'Scope data per user' (Step 4) covers this too — without this filter,
    any logged-in user could list every document in the system.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Document).where(Document.user_id == current_user.id)
        )
        docs = result.scalars().all()
        return [
            {
                "id": str(d.id),
                "filename": d.filename,
                "num_pages": d.num_pages,
                "status": d.status,
                "created_at": d.created_at,
            }
            for d in docs
        ]