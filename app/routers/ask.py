from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.search import search_chunks
from app.services.context_builder import build_context
from app.services.prompt_builder import build_prompt
from app.services.llm import stream_answer
from app.core.dependencies import get_current_user
from app.services.hybrid_search import hybrid_search

from app.models import User, ChatMessage
from app.db.db import AsyncSessionLocal
import time
import logging

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

"""
@router.post("/ask")
async def ask(request: AskRequest, current_user: User = Depends(get_current_user)):
    chunks = await search_chunks(request.question, top_k=request.top_k,user_id=str(current_user.id))
    context = build_context(chunks)
    messages = build_prompt(request.question, context)

    async def event_generator():
        async for token in stream_answer(messages):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
    """

@router.post("/ask")
async def ask(
    request: AskRequest,
    current_user: User = Depends(get_current_user)
):
    request_start = time.perf_counter()

    retrieval_start = time.perf_counter()

    chunks = await hybrid_search(
        request.question,
        top_k=request.top_k,
        user_id=str(current_user.id)
    )

    retrieval_time = time.perf_counter() - retrieval_start

    context = build_context(chunks)
    messages = build_prompt(request.question, context)

    async def event_generator():
        answer_parts = []

        llm_start = time.perf_counter()

        async for token in stream_answer(messages):
            answer_parts.append(token)
            yield f"data: {token}\n\n"

        llm_time = time.perf_counter() - llm_start

        answer = "".join(answer_parts)

        total_time = time.perf_counter() - request_start

        logging.info(
            "ask completed | "
            f"retrieval={retrieval_time:.3f}s | "
            f"llm={llm_time:.3f}s | "
            f"total={total_time:.3f}s"
        )

        source_document_ids = ",".join(
            dict.fromkeys(
                str(chunk["document_id"])
                for chunk in chunks
            )
        )

        async with AsyncSessionLocal() as session:
            chat_message = ChatMessage(
                user_id=current_user.id,
                question=request.question,
                answer=answer,
                source_document_ids=source_document_ids or None,
            )

            session.add(chat_message)
            await session.commit()

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

    
