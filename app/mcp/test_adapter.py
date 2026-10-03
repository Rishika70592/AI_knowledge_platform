import asyncio

from app.mcp.client import MCPClient
from app.mcp.tool_adapter import MCPToolAdapter


async def main():

    # -------------------------------------------------
    # 1. Create MCP client
    # -------------------------------------------------

    client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.filesystem_server",
        ],
    )

    try:

        # -------------------------------------------------
        # 2. Connect to MCP server
        # -------------------------------------------------

        await client.connect()

        # -------------------------------------------------
        # 3. Create adapter for read_file
        # -------------------------------------------------

        read_file_tool = MCPToolAdapter(
            client=client,
            tool_name="read_file",
        )

        # -------------------------------------------------
        # 4. Execute MCP tool through adapter
        # -------------------------------------------------

        result = await read_file_tool.execute(
            {
                "path": "mcp_test.txt",
            }
        )

        # -------------------------------------------------
        # 5. Print result
        # -------------------------------------------------

        print("\nAdapter result:")
        print(result)

    finally:

        # -------------------------------------------------
        # 6. Close MCP connection
        # -------------------------------------------------

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
