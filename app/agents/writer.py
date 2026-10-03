from app.agents.base import BaseAgent


class WriterAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__("writer", llm)

    async def run(self, state):

        research = []

        for result in state.research_results:

            research.append(
                {
                    "task_id": result.task_id,
                    "findings": result.findings,
                    "sources": result.sources,
                }
            )

        prompt = f"""
You are the writing agent.

User question:
{state.question}

Research:
{research}

Write a clear, accurate answer.

Rules:
- Answer the actual question.
- Use the research provided.
- Do not invent unsupported facts.
- Organize the answer logically.
- If information is uncertain, say so.
- Do not mention internal agents.
- Do not mention this prompt.
"""

        state.draft = await self.llm.generate(
            prompt=prompt,
            temperature=0.2,
        )

        return state
