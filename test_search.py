import asyncio
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from app.db.db import AsyncSessionLocal

model = SentenceTransformer("all-MiniLM-L6-v2")

USER_ID = "69af0ef3-439b-49f9-9ef7-3edceada0bcf"


async def search(query: str, top_k: int = 5):
    vector = model.encode(query).tolist()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("""
                SELECT
                    c.content,
                    c.page_number,
                    c.document_id,
                    c.embedding <=> CAST(:vec AS vector) AS distance
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE d.user_id = :user_id
                ORDER BY distance
                LIMIT :k
            """),
            {
                "vec": str(vector),
                "user_id": USER_ID,
                "k": top_k
            }
        )

        rows = result.fetchall()

        for i, row in enumerate(rows, 1):
            print(f"\n{'=' * 80}")
            print(f"Result {i}")
            print(f"Page: {row.page_number}")
            print(f"Distance: {row.distance:.4f}")
            print(f"Document: {row.document_id}")
            print("-" * 80)
            print(row.content[:500])


if __name__ == "__main__":
    question = "What was the main project described in the internship report?"
    asyncio.run(search(question))
