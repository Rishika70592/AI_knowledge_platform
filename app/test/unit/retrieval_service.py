import pytest

from app.services.retrieval_service import RetrievalService


@pytest.mark.asyncio
async def test_search_returns_results(monkeypatch):

    fake_results = [
        {
            "document_id": "doc1",
            "page_number": 1,
            "content": "RAG uses retrieval before generation.",
            "score": 0.95,
        }
    ]

    async def fake_search_chunks(
        query,
        top_k,
        user_id,
        document_id,
    ):
        return fake_results

    monkeypatch.setattr(
        "app.services.retrieval_service.search_chunks",
        fake_search_chunks,
    )

    service = RetrievalService()

    results = await service.search(
        query="What is RAG?",
        top_k=5,
        user_id="user1",
    )

    assert results == fake_results


@pytest.mark.asyncio
async def test_search_passes_arguments_correctly(monkeypatch):

    received = {}

    async def fake_search_chunks(
        query,
        top_k,
        user_id,
        document_id,
    ):
        received["query"] = query
        received["top_k"] = top_k
        received["user_id"] = user_id
        received["document_id"] = document_id

        return []

    monkeypatch.setattr(
        "app.services.retrieval_service.search_chunks",
        fake_search_chunks,
    )

    service = RetrievalService()

    await service.search(
        query="Explain embeddings",
        top_k=10,
        user_id="user123",
        document_id="doc456",
    )

    assert received["query"] == "Explain embeddings"
    assert received["top_k"] == 10
    assert received["user_id"] == "user123"
    assert received["document_id"] == "doc456"


@pytest.mark.asyncio
async def test_search_uses_default_values(monkeypatch):

    received = {}

    async def fake_search_chunks(
        query,
        top_k,
        user_id,
        document_id,
    ):
        received["query"] = query
        received["top_k"] = top_k
        received["user_id"] = user_id
        received["document_id"] = document_id

        return []

    monkeypatch.setattr(
        "app.services.retrieval_service.search_chunks",
        fake_search_chunks,
    )

    service = RetrievalService()

    await service.search("What is RAG?")

    assert received["query"] == "What is RAG?"
    assert received["top_k"] == 5
    assert received["user_id"] is None
    assert received["document_id"] is None
