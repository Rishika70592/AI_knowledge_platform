import pytest

from app.services.hybrid_search import hybrid_search
from app.services.context_builder import build_context


@pytest.mark.asyncio
async def test_hybrid_search_builds_context(monkeypatch):

    vector_results = [
        {
            "document_id": "doc1",
            "page_number": 1,
            "content": "RAG uses retrieval to find relevant information.",
            "score": 0.9,
        },
        {
            "document_id": "doc2",
            "page_number": 2,
            "content": "Vector search finds semantically similar text.",
            "score": 0.8,
        },
    ]

    keyword_results = [
        {
            "document_id": "doc1",
            "page_number": 1,
            "content": "RAG uses retrieval to find relevant information.",
            "score": 0.7,
        },
    ]

    async def fake_vector_search(query, top_k=10, user_id=None):
        return vector_results

    async def fake_keyword_search(query, top_k=10, user_id=None):
        return keyword_results

    monkeypatch.setattr(
        "app.services.hybrid_search.search_chunks",
        fake_vector_search,
    )

    monkeypatch.setattr(
        "app.services.hybrid_search.keyword_search",
        fake_keyword_search,
    )

    chunks = await hybrid_search(
        query="What is RAG?",
        top_k=5,
    )

    context = build_context(chunks)

    assert isinstance(context, str)

    assert "RAG uses retrieval" in context

    assert "Vector search" in context

    assert "[Source 1, Page 1]" in context
