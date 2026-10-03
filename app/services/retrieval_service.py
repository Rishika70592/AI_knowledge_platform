from app.services.search import search_chunks


class RetrievalService:

    async def search(
        self,
        query: str,
        top_k: int = 5,
        user_id: str | None = None,
        document_id: str | None = None,
    ):

        results = await search_chunks(
            query=query,
            top_k=top_k,
            user_id=user_id,
            document_id=document_id,
        )

        return results
