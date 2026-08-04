import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.chat_services import generate_response
from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)



router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    answer = generate_response(request.message)

    return ChatResponse(
        answer=answer
    )
# Streaming generator
async def answer_stream():

    words = [
        "Artificial",
        "Intelligence",
        "is",
        "the",
        "future"
    ]

    for word in words:
        yield word + " "
        await asyncio.sleep(1)


# Streaming endpoint
@router.post("/chat/stream")
def stream_chat():

    return StreamingResponse(
        answer_stream(),
        media_type="text/event-stream"
    )