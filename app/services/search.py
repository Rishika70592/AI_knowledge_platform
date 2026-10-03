import asyncio
import os

from sentence_transformers import SentenceTransformer
from sqlalchemy import text

from app.db.db import AsyncSessionLocal


os.environ.setdefault("HF_HUB_OFFLINE", "1")

model = SentenceTransformer("all-MiniLM-L6-v2")


async def search_chunks(
    query: str,
    top_k: int = 5,
    document_id: str | None = None,
    user_id: str | None = None,
):
    """
    Semantic vector search over document chunks.

    Returns dictionaries so the agent layer does not depend
    on SQLAlchemy row objects.
    """

    loop = asyncio.get_running_loop()

    vector = await loop.run_in_executor(
        None,
        model.encode,
        query,
    )

    vector = vector.tolist()

    async with AsyncSessionLocal() as session:

        conditions = []
        params = {
            "vec": str(vector),
            "k": top_k,
        }

        if document_id:
            conditions.append(
                "c.document_id = :document_id"
            )

            params["document_id"] = document_id

        if user_id:
            conditions.append(
                "d.user_id = :user_id"
            )

            params["user_id"] = user_id

        where_clause = ""

        if conditions:
            where_clause = (
                "WHERE " +
                " AND ".join(conditions)
            )

        query_sql = f"""
            SELECT
                c.content,
                c.page_number,
                c.document_id,
                c.embedding <=> CAST(
                    :vec AS vector
                ) AS distance

            FROM chunks c

            JOIN documents d
                ON c.document_id = d.id

            {where_clause}

            ORDER BY distance

            LIMIT :k
        """

        result = await session.execute(
            text(query_sql),
            params,
        )

        rows = result.fetchall()

    return [
        {
            "content": row.content,
            "page_number": row.page_number,
            "document_id": str(row.document_id),
            "distance": float(row.distance),
            "score": 1.0 - float(row.distance),
        }
        for row in rows
    ]
