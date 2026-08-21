import ollama
from app.core.config import LLM_MODEL
import asyncio

async def stream_answer(messages: list[dict]):
    loop = asyncio.get_event_loop()

    def _stream():
        return ollama.chat(model=LLM_MODEL, messages=messages, stream=True)

    stream = await loop.run_in_executor(None, _stream)

    for chunk in stream:
        token = chunk["message"]["content"]
        if token:
            yield token
            await asyncio.sleep(0)