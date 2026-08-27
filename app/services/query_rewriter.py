import ollama
from app.core.config import LLM_MODEL
import asyncio

async def rewrite_query(raw_question: str, domain_context: str = None) -> str:
    loop = asyncio.get_event_loop()

    domain_hint = (
        f"The user is asking about the following domain: {domain_context}. "
        if domain_context else ""
    )

    messages = [
        {
            "role": "system",
            "content": (
                f"{domain_hint}"
                "Rewrite the user's question to be clearer and more specific, "
                "WITHOUT changing its actual topic or introducing new subjects "
                "not implied by the original question. If the question is "
                "already clear, return it unchanged. Keep it concise — one "
                "sentence. Return ONLY the rewritten question, nothing else."
            )
        },
        {"role": "user", "content": raw_question}
    ]

    def _call():
        return ollama.chat(model=LLM_MODEL, messages=messages, stream=False)

    response = await loop.run_in_executor(None, _call)
    return response["message"]["content"].strip()