import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.github_server"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available GitHub tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\nSearching GitHub...")

            result = await session.call_tool(
                "search_repositories",
                {
                    "query": "fastapi"
                }
            )

            print("\nSearch result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
