from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.search import search_chunks
from app.services.context_builder import build_context
from app.services.prompt_builder import build_prompt
from app.services.llm import stream_answer

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/ask")
async def ask(request: AskRequest):
    chunks = await search_chunks(request.question, top_k=request.top_k)
    context = build_context(chunks)
    messages = build_prompt(request.question, context)

    async def event_generator():
        async for token in stream_answer(messages):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")