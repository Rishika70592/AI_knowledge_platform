import asyncio
from app.services.query_rewriter import rewrite_query

async def main():
    domain = "an internship report about robotics, Arduino electronics projects, and workshops at a company called Robozonix"
    vague_questions = [
        "what about the fee",
        "tell me about the hours thing",
        "who's in charge",
    ]
    for q in vague_questions:
        rewritten = await rewrite_query(q)
        print(f"Original:  {q}")
        print(f"Rewritten: {rewritten}\n")

asyncio.run(main())