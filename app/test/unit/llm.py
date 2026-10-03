import pytest
from unittest.mock import patch

from app.services.llm import stream_answer


@pytest.mark.asyncio
async def test_stream_answer_yields_tokens():
    fake_stream = [
        {"message": {"content": "Hello"}},
        {"message": {"content": " world"}},
        {"message": {"content": "!"}},
    ]

    with patch("app.services.llm.ollama.chat") as mock_chat:
        mock_chat.return_value = fake_stream

        messages = [
            {"role": "user", "content": "Say hello"}
        ]

        result = []

        async for token in stream_answer(messages):
            result.append(token)

    assert result == ["Hello", " world", "!"]


@pytest.mark.asyncio
async def test_stream_answer_calls_ollama():
    fake_stream = [
        {"message": {"content": "Hello"}}
    ]

    with patch("app.services.llm.ollama.chat") as mock_chat:
        mock_chat.return_value = fake_stream

        messages = [
            {"role": "user", "content": "Say hello"}
        ]

        result = []

        async for token in stream_answer(messages):
            result.append(token)

        mock_chat.assert_called_once_with(
            model=mock_chat.call_args.kwargs["model"],
            messages=messages,
            stream=True,
        )


@pytest.mark.asyncio
async def test_stream_answer_skips_empty_tokens():
    fake_stream = [
        {"message": {"content": ""}},
        {"message": {"content": "Hello"}},
        {"message": {"content": ""}},
        {"message": {"content": "!"}},
    ]

    with patch("app.services.llm.ollama.chat") as mock_chat:
        mock_chat.return_value = fake_stream

        result = []

        async for token in stream_answer(
            [{"role": "user", "content": "Say hello"}]
        ):
            result.append(token)

    assert result == ["Hello", "!"]
