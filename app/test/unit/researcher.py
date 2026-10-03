import pytest

from app.agents.researcher import ResearchAgent
from app.agents.state import AgentState
from app.schemas.agent import Plan, ResearchTask


class FakeLLM:

    def __init__(self, response="Research finding"):
        self.response = response
        self.called = False

    async def generate(self, prompt, temperature=0.1):
        self.called = True
        return self.response


class FakeRetriever:

    def __init__(self):
        self.called = False
        self.last_query = None

    async def search(self, query, top_k=5, user_id=None):
        self.called = True
        self.last_query = query

        return [
            {
                "document_id": "doc1",
                "page_number": 1,
                "content": "RAG combines retrieval with generation.",
                "score": 0.95,
                "distance": 0.05,
            }
        ]


def make_state():
    state = AgentState(
        question="What is RAG?",
        user_id="user1",
    )

    task = ResearchTask(
        question="What is retrieval augmented generation?",
        purpose="Understand RAG.",
    )

    state.plan = Plan(
        original_question=state.question,
        tasks=[task],
    )

    return state


@pytest.mark.asyncio
async def test_researcher_returns_state_when_no_plan():

    llm = FakeLLM()
    retriever = FakeRetriever()

    agent = ResearchAgent(llm, retriever)

    state = AgentState(
        question="What is RAG?"
    )

    result = await agent.run(state)

    assert result is state
    assert result.research_results == []


@pytest.mark.asyncio
async def test_researcher_returns_state_when_no_retriever():

    llm = FakeLLM()

    agent = ResearchAgent(
        llm,
        None,
    )

    state = make_state()

    result = await agent.run(state)

    assert result is state
    assert result.research_results == []


@pytest.mark.asyncio
async def test_researcher_calls_retriever():

    llm = FakeLLM()
    retriever = FakeRetriever()

    agent = ResearchAgent(
        llm,
        retriever,
    )

    state = make_state()

    await agent.run(state)

    assert retriever.called is True
    assert (
        retriever.last_query
        == "What is retrieval augmented generation?"
    )


@pytest.mark.asyncio
async def test_researcher_calls_llm():

    llm = FakeLLM(
        "RAG retrieves relevant information before generation."
    )

    retriever = FakeRetriever()

    agent = ResearchAgent(
        llm,
        retriever,
    )

    state = make_state()

    await agent.run(state)

    assert llm.called is True


@pytest.mark.asyncio
async def test_researcher_creates_research_result():

    llm = FakeLLM(
        "RAG retrieves relevant information before generation."
    )

    retriever = FakeRetriever()

    agent = ResearchAgent(
        llm,
        retriever,
    )

    state = make_state()

    result = await agent.run(state)

    assert len(result.research_results) == 1

    research_result = result.research_results[0]

    assert research_result.findings == [
        "RAG retrieves relevant information before generation."
    ]

    assert len(research_result.sources) == 1

    assert research_result.sources[0]["document_id"] == "doc1"
    assert research_result.sources[0]["page_number"] == 1
