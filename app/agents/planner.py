import json

from app.agents.base import BaseAgent
from app.schemas.agent import Plan, ResearchTask


class PlannerAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__("planner", llm)

    async def run(self, state):

        prompt = f"""
You are a research planning agent.

Your job is to decompose the user's question into 2 to 4
specific and non-overlapping research tasks.

User question:
{state.question}

Return ONLY valid JSON:

{{
  "tasks": [
    {{
      "question": "specific research question",
      "purpose": "why this research is necessary"
    }}
  ]
}}

Rules:
- Create between 2 and 4 tasks.
- Do not answer the user's question.
- Each task must investigate a different aspect.
- Tasks must be specific and independently researchable.
- Avoid duplicate or overlapping tasks.
- Do not include commentary outside the JSON.
"""

        response = await self.llm.generate(
            prompt=prompt,
            temperature=0.1,
        )

        try:
            data = json.loads(response)

            raw_tasks = data.get("tasks")

            if not isinstance(raw_tasks, list):
                raise ValueError("tasks must be a list")

            if not 2 <= len(raw_tasks) <= 4:
                raise ValueError("planner must create 2-4 tasks")

            tasks = []

            for item in raw_tasks:

                if not isinstance(item, dict):
                    raise ValueError("task must be an object")

                question = item.get("question")
                purpose = item.get("purpose")

                if not question or not purpose:
                    raise ValueError(
                        "task requires question and purpose"
                    )

                tasks.append(
                    ResearchTask(
                        question=question,
                        purpose=purpose,
                    )
                )

        except (json.JSONDecodeError, ValueError, TypeError):

            tasks = [
                ResearchTask(
                    question=state.question,
                    purpose="Research the user's question.",
                )
            ]

        state.plan = Plan(
            original_question=state.question,
            tasks=tasks,
        )

        return state
