import os
os.environ["HF_HUB_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from app.db.db import AsyncSessionLocal
import asyncio

model = SentenceTransformer("all-MiniLM-L6-v2")

async def search_chunks(query: str, top_k: int = 5):
    loop = asyncio.get_event_loop()
    vector = await loop.run_in_executor(None, model.encode, query)
    vector = vector.tolist()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("""
                SELECT content, page_number, document_id,
                       embedding <=> CAST(:vec AS vector) AS distance
                FROM chunks
                ORDER BY distance
                LIMIT :k
            """),
            {"vec": str(vector), "k": top_k}
        )
        rows = result.fetchall()
        return [
            {
                "content": row.content,
                "page_number": row.page_number,
                "document_id": str(row.document_id),
                "distance": row.distance,
            }
            for row in rows
        ]