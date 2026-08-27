from sqlalchemy import text
from app.db.db import AsyncSessionLocal

async def keyword_search(query: str, top_k: int = 5):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("""
                SELECT content, page_number, document_id,
                       ts_rank(content_tsv, plainto_tsquery('english', :query)) AS score
                FROM chunks
                WHERE content_tsv @@ plainto_tsquery('english', :query)
                ORDER BY score DESC
                LIMIT :k
            """),
            {"query": query, "k": top_k}
        )
        rows = result.fetchall()
        return [
            {
                "content": row.content,
                "page_number": row.page_number,
                "document_id": str(row.document_id),
                "score": row.score,
            }
            for row in rows
        ]