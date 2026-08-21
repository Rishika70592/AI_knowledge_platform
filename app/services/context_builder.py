def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Source {i}, Page {chunk['page_number']}]\n{chunk['content']}"
        )
    return "\n\n".join(parts)