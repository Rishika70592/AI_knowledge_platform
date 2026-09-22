import os
os.environ["HF_HUB_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from app.db.db import AsyncSessionLocal
import asyncio

model = SentenceTransformer("all-MiniLM-L6-v2")

async def search_chunks(query: str, top_k: int = 5, document_id: str = None,user_id: str = None):
    loop = asyncio.get_event_loop()
    vector = await loop.run_in_executor(None, model.encode, query)
    vector = vector.tolist()

    

    async with AsyncSessionLocal() as session:
        conditions = []
        params = {"vec": str(vector), "k": top_k}

        if document_id:
            conditions.append("c.document_id = :doc_id")
            params["doc_id"] = document_id
        if user_id:
            conditions.append("d.user_id = :user_id")
            params["user_id"] = user_id

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        sql = f"""
            SELECT c.content, c.page_number, c.document_id,
                   c.embedding <=> CAST(:vec AS vector) AS distance
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            {where_clause}
            ORDER BY distance
            LIMIT :k
        """

        result = await session.execute(text(sql), params)
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