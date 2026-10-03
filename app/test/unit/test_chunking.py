from app.services.chunking import chunk_text


def test_chunk_text_returns_list():
    result = chunk_text("Hello world")

    assert isinstance(result, list)


def test_chunk_text_does_not_return_empty_list():
    result = chunk_text("Hello world")

    assert len(result) > 0
