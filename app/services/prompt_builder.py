def build_prompt(question: str, context: str) -> list[dict]:
    system_prompt = (
        "You are a helpful assistant answering questions using ONLY the "
        "provided context below. If the answer is not contained in the "
        "context, say you don't know — do not make up information. "
        "When you use information from a source, mention which source "
        "number it came from."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]