from typing import Any


class KnowledgeBaseTools:

    def __init__(self, retrieval_service=None):
        self.retrieval_service = retrieval_service

    async def search_knowledge_base(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:

        if self.retrieval_service is None:
            return {
                "query": query,
                "results": [],
                "error": "Knowledge base retrieval is not configured.",
            }

        try:

            results = await self.retrieval_service.search(
                query=query,
                top_k=top_k,
            )

        except Exception as exc:

            return {
                "query": query,
                "results": [],
                "error": f"Knowledge base search failed: {exc}",
            }

        formatted_results = []

        for result in results:

            formatted_results.append(
                {
                    "content": result.get(
                        "content",
                        "",
                    ),
                    "page_number": result.get(
                        "page_number",
                    ),
                    "document_id": result.get(
                        "document_id",
                    ),
                    "distance": result.get(
                        "distance",
                    ),
                }
            )

        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results),
        }
