import asyncio
from app.services.hybrid_search import hybrid_search

async def main():
    results = await hybrid_search("Who supervised the internship and what is their designation")
    for r in results:
        print(f"\n[Page {r['page_number']}]")
        print(r['content'][:200])

asyncio.run(main())