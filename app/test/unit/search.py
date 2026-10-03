import pytest
import numpy as np
from app.services import search


class FakeModel:

    def encode(self, query):
        assert query == "What is RAG?"

        return np.array([0.1, 0.2, 0.3])


class FakeResult:

    def fetchall(self):

        Row = type(
            "Row",
            (),
            {
                "content": "RAG retrieves relevant documents.",
                "page_number": 2,
                "document_id": "doc123",
                "distance": 0.2,
            },
        )

        return [Row()]


class FakeSession:

    def __init__(self):
        self.executed_sql = None
        self.executed_params = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def execute(self, sql, params):
        self.executed_sql = sql
        self.executed_params = params

        return FakeResult()


class FakeSessionFactory:

    def __init__(self, session):
        self.session = session

    def __call__(self):
        return self.session


@pytest.mark.asyncio
async def test_search_chunks_returns_results(monkeypatch):

    fake_session = FakeSession()

    monkeypatch.setattr(
        search,
        "model",
        FakeModel(),
    )

    monkeypatch.setattr(
        search,
        "AsyncSessionLocal",
        FakeSessionFactory(fake_session),
    )

    results = await search.search_chunks(
        query="What is RAG?",
        top_k=5,
    )

    assert len(results) == 1

    assert results[0]["content"] == (
        "RAG retrieves relevant documents."
    )

    assert results[0]["page_number"] == 2
    assert results[0]["document_id"] == "doc123"
    assert results[0]["distance"] == 0.2
    assert results[0]["score"] == 0.8


@pytest.mark.asyncio
async def test_search_chunks_passes_top_k(monkeypatch):

    fake_session = FakeSession()

    monkeypatch.setattr(
        search,
        "model",
        FakeModel(),
    )

    monkeypatch.setattr(
        search,
        "AsyncSessionLocal",
        FakeSessionFactory(fake_session),
    )

    await search.search_chunks(
        query="What is RAG?",
        top_k=10,
    )

    assert fake_session.executed_params["k"] == 10


@pytest.mark.asyncio
async def test_search_chunks_applies_document_filter(monkeypatch):

    fake_session = FakeSession()

    monkeypatch.setattr(
        search,
        "model",
        FakeModel(),
    )

    monkeypatch.setattr(
        search,
        "AsyncSessionLocal",
        FakeSessionFactory(fake_session),
    )

    await search.search_chunks(
        query="What is RAG?",
        top_k=5,
        document_id="doc123",
    )

    assert (
        "c.document_id = :document_id"
        in str(fake_session.executed_sql)
    )

    assert (
        fake_session.executed_params["document_id"]
        == "doc123"
    )


@pytest.mark.asyncio
async def test_search_chunks_applies_user_filter(monkeypatch):

    fake_session = FakeSession()

    monkeypatch.setattr(
        search,
        "model",
        FakeModel(),
    )

    monkeypatch.setattr(
        search,
        "AsyncSessionLocal",
        FakeSessionFactory(fake_session),
    )

    await search.search_chunks(
        query="What is RAG?",
        top_k=5,
        user_id="user123",
    )

    assert (
        "d.user_id = :user_id"
        in str(fake_session.executed_sql)
    )

    assert (
        fake_session.executed_params["user_id"]
        == "user123"
    )
