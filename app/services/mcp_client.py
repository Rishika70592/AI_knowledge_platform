import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def get_database_tables():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.postgres_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "list_tables",
                {}
            )

            return result
