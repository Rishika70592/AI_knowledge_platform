from app.services.cleaning import clean_text


def test_clean_text_returns_string():
    result = clean_text("Hello world")

    assert isinstance(result, str)
