from unittest.mock import patch

import pytest

from app.services.embeddings import embed_texts


@pytest.mark.asyncio
async def test_embed_texts_returns_list():
    fake_embeddings = [[0.1, 0.2, 0.3]]

    with patch("app.services.embeddings.model.encode") as mock_encode:
        mock_encode.return_value.tolist.return_value = fake_embeddings

        result = await embed_texts(["Hello world"])

    assert isinstance(result, list)
    assert result == fake_embeddings


@pytest.mark.asyncio
async def test_embed_texts_calls_model():
    fake_embeddings = [[0.1, 0.2, 0.3]]

    with patch("app.services.embeddings.model.encode") as mock_encode:
        mock_encode.return_value.tolist.return_value = fake_embeddings

        await embed_texts(["Hello world", "How are you?"])

        mock_encode.assert_called_once_with(
            ["Hello world", "How are you?"],
            convert_to_numpy=True,
        )


@pytest.mark.asyncio
async def test_embed_texts_returns_one_embedding_per_text():
    fake_embeddings = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    with patch("app.services.embeddings.model.encode") as mock_encode:
        mock_encode.return_value.tolist.return_value = fake_embeddings

        result = await embed_texts(["Hello", "World"])

    assert len(result) == 2
