from unittest.mock import AsyncMock

import pytest

from app.agents.planner import PlannerAgent
from app.agents.state import AgentState


class FakeLLM:
    def __init__(self, response):
        self.generate = AsyncMock(return_value=response)


def make_state(question="What is retrieval augmented generation?"):
    return AgentState(question=question)


@pytest.mark.asyncio
async def test_planner_creates_valid_plan():
    response = """
    {
        "tasks": [
            {
                "question": "What is retrieval augmented generation?",
                "purpose": "Understand the basic concept."
            },
            {
                "question": "How does vector search support RAG?",
                "purpose": "Understand the retrieval component."
            }
        ]
    }
    """

    llm = FakeLLM(response)
    agent = PlannerAgent(llm)

    state = make_state()

    result = await agent.run(state)

    assert result.plan is not None
    assert result.plan.original_question == state.question
    assert len(result.plan.tasks) == 2


@pytest.mark.asyncio
async def test_planner_creates_research_tasks():
    response = """
    {
        "tasks": [
            {
                "question": "What is RAG?",
                "purpose": "Understand RAG."
            },
            {
                "question": "What is vector search?",
                "purpose": "Understand retrieval."
            }
        ]
    }
    """

    llm = FakeLLM(response)
    agent = PlannerAgent(llm)

    result = await agent.run(make_state())

    assert result.plan.tasks[0].question == "What is RAG?"
    assert result.plan.tasks[0].purpose == "Understand RAG."


@pytest.mark.asyncio
async def test_planner_calls_llm():
    response = """
    {
        "tasks": [
            {
                "question": "What is RAG?",
                "purpose": "Understand RAG."
            },
            {
                "question": "How does retrieval work?",
                "purpose": "Understand retrieval."
            }
        ]
    }
    """

    llm = FakeLLM(response)
    agent = PlannerAgent(llm)

    state = make_state()

    await agent.run(state)

    llm.generate.assert_awaited_once()

    call = llm.generate.call_args

    assert state.question in call.kwargs["prompt"]
    assert call.kwargs["temperature"] == 0.1


@pytest.mark.asyncio
async def test_planner_falls_back_on_invalid_json():
    llm = FakeLLM("this is not valid JSON")

    agent = PlannerAgent(llm)

    state = make_state("Explain embeddings")

    result = await agent.run(state)

    assert result.plan is not None
    assert len(result.plan.tasks) == 1
    assert result.plan.tasks[0].question == "Explain embeddings"


@pytest.mark.asyncio
async def test_planner_falls_back_when_task_count_is_invalid():
    response = """
    {
        "tasks": [
            {
                "question": "What is RAG?",
                "purpose": "Understand RAG."
            }
        ]
    }
    """

    llm = FakeLLM(response)
    agent = PlannerAgent(llm)

    state = make_state("Explain RAG")

    result = await agent.run(state)

    assert len(result.plan.tasks) == 1
    assert result.plan.tasks[0].question == "Explain RAG"
