from app.agents.base import BaseAgent


class ReflectionAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__("reflection", llm)

    async def run(self, state):

        if state.review is None:
            return state

        if state.review.approved:
            state.final_answer = state.draft
            return state

        prompt = f"""
You are a reflection agent.

Original question:
{state.question}

Current draft:
{state.draft}

Reviewer feedback:
{state.review.model_dump()}

Improve the answer.

Rules:
- Fix every issue that can be fixed.
- Keep supported facts.
- Remove unsupported claims.
- Answer the original question directly.
- Return ONLY the revised answer.
"""

        revised = await self.llm.generate(
            prompt=prompt,
            temperature=0.15,
        )

        state.draft = revised

        return state
