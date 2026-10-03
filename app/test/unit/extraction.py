from io import BytesIO

from pypdf import PdfWriter

from app.services.extraction import extract_text_by_page


def create_test_pdf(text_pages: list[str]) -> bytes:
    writer = PdfWriter()

    for text in text_pages:
        writer.add_blank_page(width=300, height=300)

    output = BytesIO()
    writer.write(output)

    return output.getvalue()


def test_extract_text_by_page_returns_list():
    pdf_bytes = create_test_pdf(["Hello"])

    result = extract_text_by_page(pdf_bytes)

    assert isinstance(result, list)


def test_extract_text_by_page_returns_page_numbers():
    pdf_bytes = create_test_pdf(["Page 1", "Page 2"])

    result = extract_text_by_page(pdf_bytes)

    assert len(result) == 2
    assert result[0]["page_number"] == 1
    assert result[1]["page_number"] == 2


def test_extract_text_by_page_returns_expected_structure():
    pdf_bytes = create_test_pdf(["Hello"])

    result = extract_text_by_page(pdf_bytes)

    assert isinstance(result[0], dict)
    assert "page_number" in result[0]
    assert "text" in result[0]
