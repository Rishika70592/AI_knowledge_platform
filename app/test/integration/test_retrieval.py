import pytest

from app.services.retrieval_service import RetrievalService


@pytest.mark.asyncio
async def test_retrieval_service_search():

    service = RetrievalService()

    results = await service.search(
        query="What is RAG?",
        top_k=5,
    )

    assert isinstance(results, list)
