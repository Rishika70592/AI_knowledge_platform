import asyncio

from app.mcp.client import MCPClient


async def main():

    client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.filesystem_server",
        ],
    )

    try:

        await client.connect()

        tools = await client.list_tools()

        print("Available tools:")

        for tool in tools:
            print(
                f"- {tool.name}: "
                f"{tool.description}"
            )

        result = await client.call_tool(
            "read_file",
            {
                "path": "mcp_test.txt",
            },
        )

        print("\nResult:")
        print(result)

    finally:

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
