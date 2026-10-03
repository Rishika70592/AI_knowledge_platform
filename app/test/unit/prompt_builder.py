from app.services.prompt_builder import build_prompt


def test_build_prompt_returns_list():
    result = build_prompt(
        "What is RAG?",
        "RAG means Retrieval-Augmented Generation."
    )

    assert isinstance(result, list)


def test_build_prompt_returns_two_messages():
    result = build_prompt(
        "What is RAG?",
        "RAG means Retrieval-Augmented Generation."
    )

    assert len(result) == 2


def test_build_prompt_has_correct_roles():
    result = build_prompt(
        "What is RAG?",
        "RAG means Retrieval-Augmented Generation."
    )

    assert result[0]["role"] == "system"
    assert result[1]["role"] == "user"


def test_build_prompt_contains_context_and_question():
    question = "What is RAG?"
    context = "RAG means Retrieval-Augmented Generation."

    result = build_prompt(question, context)

    assert context in result[1]["content"]
    assert question in result[1]["content"]


def test_build_prompt_system_instruction():
    result = build_prompt(
        "What is RAG?",
        "RAG means Retrieval-Augmented Generation."
    )

    system_content = result[0]["content"]

    assert "ONLY" in system_content
    assert "don't know" in system_content
    assert "do not make up information" in system_content
    assert "source number" in system_content
