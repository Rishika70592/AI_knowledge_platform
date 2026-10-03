from app.agents.base import BaseAgent
from app.schemas.agent import ResearchResult


class ResearchAgent(BaseAgent):

    def __init__(
        self,
        llm,
        retriever,
    ):
        super().__init__(
            "researcher",
            llm,
        )

        self.retriever = retriever

    async def run(self, state):

        if state.plan is None:
            return state

        if self.retriever is None:
            return state

        for task in state.plan.tasks:

            # --------------------------------------------------
            # 1. Retrieve evidence
            # --------------------------------------------------

            retrieved_information = await self.retriever.search(
                query=task.question,
                top_k=5,
                user_id=state.user_id,
            )

            # --------------------------------------------------
            # 2. Format evidence
            # --------------------------------------------------

            evidence = []

            for item in retrieved_information:

                evidence.append(
                    {
                        "document_id": item.get(
                            "document_id"
                        ),
                        "page_number": item.get(
                            "page_number"
                        ),
                        "content": item.get(
                            "content",
                            item.get("text", ""),
                        ),
                        "score": item.get(
                            "score"
                        ),
                        "distance": item.get(
                            "distance"
                        ),
                    }
                )

            # --------------------------------------------------
            # 3. Research prompt
            # --------------------------------------------------

            prompt = f"""
You are a research agent.

Research task:
{task.question}

Purpose:
{task.purpose}

Retrieved evidence:
{evidence}

Extract the important factual findings.

Rules:
- Use ONLY the retrieved evidence.
- Do not use outside knowledge.
- Do not invent facts.
- If evidence is insufficient, explicitly say so.
- Keep findings concise.
- Preserve important details.
- Do not make unsupported conclusions.
"""

            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.1,
            )

            # --------------------------------------------------
            # 4. Sources
            # --------------------------------------------------

            sources = []

            for item in retrieved_information:

                sources.append(
                    {
                        "document_id": item.get(
                            "document_id"
                        ),
                        "page_number": item.get(
                            "page_number"
                        ),
                        "score": item.get(
                            "score"
                        ),
                    }
                )

            # --------------------------------------------------
            # 5. Store result
            # --------------------------------------------------

            result = ResearchResult(
                task_id=task.id,
                findings=[response],
                sources=sources,
                confidence=0.7,
            )

            state.research_results.append(result)

        return state
