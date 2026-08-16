import asyncio
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from app.db.db import AsyncSessionLocal

model = SentenceTransformer("all-MiniLM-L6-v2")

async def search(query: str, top_k: int = 5):
    vector = model.encode(query).tolist()
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("""
                SELECT content, embedding <=> CAST(:vec AS vector) AS distance
                FROM chunks
                ORDER BY distance
                LIMIT :k
            """),
            {"vec": str(vector), "k": top_k}
        )
        rows = result.fetchall()
        for i, row in enumerate(rows, 1):
            print(f"\n--- Result {i} (distance: {row.distance:.4f}) ---")
            print(row.content[:300])

if __name__ == "__main__":
    question = "Who is matangini hazra"
    asyncio.run(search(question))