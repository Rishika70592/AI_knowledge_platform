import asyncio

from app.mcp.client import MCPClient
from app.mcp.register_tools import register_filesystem_tools
from app.agents.tools import ToolRegistry


async def main():

    # -------------------------------------------------
    # 1. Create registry
    # -------------------------------------------------

    registry = ToolRegistry()

    # -------------------------------------------------
    # 2. Create MCP client
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
        # 3. Connect MCP
        # -------------------------------------------------

        await client.connect()

        # -------------------------------------------------
        # 4. Register MCP tools
        # -------------------------------------------------

        await register_filesystem_tools(
            tool_registry=registry,
            client=client,
        )

        # -------------------------------------------------
        # 5. Show registered tools
        # -------------------------------------------------

        print("\nRegistered tools:")

        for tool in registry.list_tools():

            print(
                f"- {tool.name}: "
                f"{tool.description}"
            )

        # -------------------------------------------------
        # 6. Execute read_file through ToolRegistry
        # -------------------------------------------------

        print("\nExecuting read_file...")

        result = await registry.execute(
            name="read_file",
            arguments={
                "path": "mcp_test.txt",
            },
        )

        print("\nResult:")
        print(result)

    finally:

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
