from app.agents.base import BaseAgent


class RetrieverAgent(BaseAgent):

    def __init__(
        self,
        llm,
        retrieval_service,
    ):
        super().__init__(
            "retriever",
            llm,
        )

        self.retrieval_service = retrieval_service

    async def search(
        self,
        query: str,
        user_id: str | None = None,
    ):

        if self.retrieval_service is None:
            return []

        return await self.retrieval_service.search(
            query=query,
            top_k=5,
            user_id=user_id,
        )

    async def run(self, state):

        if state.plan is None:
            return state

        for task in state.plan.tasks:

            results = await self.search(
                query=task.question,
                user_id=state.user_id,
            )

            task_context = []

            for result in results:

                task_context.append(
                    {
                        "content": result["content"],
                        "score": result["score"],
                        "distance": result["distance"],
                        "page_number": result["page_number"],
                        "document_id": result["document_id"],
                    }
                )

            state.memory.append(
                {
                    "type": "retrieval",
                    "task_id": task.id,
                    "query": task.question,
                    "results": task_context,
                }
            )

        return state
