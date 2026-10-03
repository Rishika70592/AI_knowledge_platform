from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.researcher import ResearchAgent
from app.agents.writer import WriterAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.reflection import ReflectionAgent
from app.agents.tool_agent import ToolCallingAgent

from app.agents.tools import ToolRegistry
from app.schemas.agent import AgentState


class AgentOrchestrator:

    def __init__(
        self,
        llm,
        retrieval_service=None,
        tool_registry: ToolRegistry | None = None,
        max_iterations: int = 2,
    ):
        self.max_iterations = max_iterations

        # 1. Planner
        self.planner = PlannerAgent(
            llm=llm,
        )

        # 2. Retriever
        self.retriever = RetrieverAgent(
            llm=llm,
            retrieval_service=retrieval_service,
        )

        # 3. Researcher
        self.researcher = ResearchAgent(
            llm=llm,
            retriever=retrieval_service,
        )

        # 4. MCP / Tool Calling Agent
        self.tool_calling = None

        if tool_registry is not None:
            self.tool_calling = ToolCallingAgent(
                llm=llm,
                tool_registry=tool_registry,
                max_steps=3,
            )

        # 5. Writer
        self.writer = WriterAgent(
            llm=llm,
        )

        # 6. Reviewer
        self.reviewer = ReviewerAgent(
            llm=llm,
        )

        # 7. Reflection
        self.reflection = ReflectionAgent(
            llm=llm,
        )

    async def run(
        self,
        question: str,
        user_id: str | None = None,
    ):

        state = AgentState(
            question=question,
            user_id=user_id,
        )

        # --------------------------------------------------
        # STEP 1: PLAN
        # --------------------------------------------------

        state = await self.planner.run(state)

        # --------------------------------------------------
        # STEP 2: RETRIEVE
        # --------------------------------------------------

        state = await self.retriever.run(state)

        # --------------------------------------------------
        # STEP 3: RESEARCH
        # --------------------------------------------------

        state = await self.researcher.run(state)

        # --------------------------------------------------
        # STEP 4: MCP TOOL CALLING
        # --------------------------------------------------

        if self.tool_calling:

            tool_answer = await self.tool_calling.run(
                question=question,
            )

            if tool_answer:

                state.tool_results.append(
                    {
                        "type": "mcp_tool_answer",
                        "question": question,
                        "answer": tool_answer,
                    }
                )

        # --------------------------------------------------
        # STEP 5: WRITE
        # --------------------------------------------------

        state = await self.writer.run(state)

        # --------------------------------------------------
        # STEP 6: REVIEW / REFLECTION LOOP
        # --------------------------------------------------

        for iteration in range(
            1,
            self.max_iterations + 1,
        ):

            state.iteration = iteration

            state = await self.reviewer.run(state)

            if (
                state.review
                and state.review.approved
            ):
                state.final_answer = state.draft
                break

            if iteration < self.max_iterations:

                state = await self.reflection.run(state)

        # --------------------------------------------------
        # STEP 7: FALLBACK
        # --------------------------------------------------

        if not state.final_answer:

            state.final_answer = (
                state.draft
                or "Unable to generate an answer."
            )

        return state
