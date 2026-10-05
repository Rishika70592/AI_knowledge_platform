import pytest

from app.services import llm


class FakeOllama:

    def chat(self, model, messages, stream):

        assert stream is True
        assert isinstance(messages, list)

        return [
            {"message": {"content": "Hello "}},
            {"message": {"content": "from "}},
            {"message": {"content": "AI!"}},
        ]


@pytest.mark.asyncio
async def test_stream_answer(monkeypatch):

    monkeypatch.setattr(
        llm,
        "ollama",
        FakeOllama(),
    )

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is RAG?",
        },
    ]

    tokens = []

    async for token in llm.stream_answer(messages):
        tokens.append(token)

    assert tokens == [
        "Hello ",
        "from ",
        "AI!",
    ]
