import asyncio
from app.services.search import search_chunks
from app.services.context_builder import build_context
from app.services.prompt_builder import build_prompt
from app.services.llm import stream_answer
async def main():
    results = await search_chunks("What robozonix did")
    for r in results:
        print(f"\n[Page {r['page_number']}] distance={r['distance']:.4f}")
        print(r['content'][:200])

    context = build_context(results)
    print("\n\n=== BUILT CONTEXT ===\n")
    print(context)


    # ... after context = build_context(results)
    messages = build_prompt("What robozonix did", context)
    print("\n\n=== BUILT PROMPT ===\n")
    for m in messages:
        print(f"[{m['role'].upper()}]")
        print(m['content'][:300])
        print()

        
        
    print("\n\n=== FULL PROMPT SENT TO LLM ===\n")
    print(messages[1]['content'])

    # ... after messages = build_prompt(...)
    print("\n\n=== LLM ANSWER ===\n")
    async for token in stream_answer(messages):
        print(token, end="", flush=True)
    print()
asyncio.run(main())