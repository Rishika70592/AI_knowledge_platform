import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.postgres_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # 1. Initialize MCP connection
            await session.initialize()

            # -------------------------------------------------
            # 2. LIST AVAILABLE TOOLS
            # -------------------------------------------------
            tools = await session.list_tools()

            print("\nAvailable tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # -------------------------------------------------
            # 3. CALL list_tables TOOL
            # -------------------------------------------------
            print("\nCalling list_tables...")

            result = await session.call_tool(
                "list_tables",
                {}
            )

            print("\nTables:")
            print(result)

            # -------------------------------------------------
            # 4. CALL describe_table TOOL
            # -------------------------------------------------
            print("\nCalling describe_table for documents...")

            result = await session.call_tool(
                "describe_table",
                {
                    "table_name": "documents"
                }
            )

            print("\nDocuments table:")
            print(result)

            # -------------------------------------------------
            # 5. READ DATABASE RESOURCE
            # -------------------------------------------------
            print("\nReading database schema...")

            result = await session.read_resource(
                "schema://database"
            )

            print("\nDatabase Schema:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
