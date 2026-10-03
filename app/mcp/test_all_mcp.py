import asyncio

from app.agents.tools import ToolRegistry

from app.mcp.client import MCPClient

from app.mcp.register_all import (
    register_all_mcp_tools,
)


async def main():

    registry = ToolRegistry()

    # =================================================
    # 1. Create Filesystem MCP client
    # =================================================

    filesystem_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.filesystem_server",
        ],
    )

    # =================================================
    # 2. Create GitHub MCP client
    # =================================================

    github_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.github_server",
        ],
    )

    # =================================================
    # 3. Create PostgreSQL MCP client
    # =================================================

    postgres_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.postgres_server",
        ],
    )

    try:

        # =================================================
        # 4. Connect all MCP servers
        # =================================================

        print("\nConnecting Filesystem MCP...")

        await filesystem_client.connect()

        print("Filesystem MCP connected.")

        print("\nConnecting GitHub MCP...")

        await github_client.connect()

        print("GitHub MCP connected.")

        print("\nConnecting PostgreSQL MCP...")

        await postgres_client.connect()

        print("PostgreSQL MCP connected.")

        # =================================================
        # 5. Register ALL tools
        # =================================================

        print("\nRegistering all MCP tools...")

        await register_all_mcp_tools(
            registry=registry,
            filesystem_client=filesystem_client,
            github_client=github_client,
            postgres_client=postgres_client,
        )

        # =================================================
        # 6. Display registered tools
        # =================================================

        print("\n===================================")
        print("Registered MCP Tools")
        print("===================================")

        for tool in registry.list_tools():

            print(
                f"- {tool.name}: "
                f"{tool.description}"
            )

        # =================================================
        # 7. Test Filesystem
        # =================================================

        print("\n===================================")
        print("Testing Filesystem MCP")
        print("===================================")

        result = await registry.execute(
            name="read_file",
            arguments={
                "path": "mcp_test.txt",
            },
        )

        print("\nread_file result:")
        print(result)

        # =================================================
        # 8. Test GitHub
        # =================================================

        print("\n===================================")
        print("Testing GitHub MCP")
        print("===================================")

        result = await registry.execute(
            name="search_repositories",
            arguments={
                "query": "fastapi",
            },
        )

        print("\nsearch_repositories result:")
        print(result)

        # =================================================
        # 9. Test PostgreSQL
        # =================================================

        print("\n===================================")
        print("Testing PostgreSQL MCP")
        print("===================================")

        result = await registry.execute(
            name="list_tables",
            arguments={},
        )

        print("\nlist_tables result:")
        print(result)

        # =================================================
        # 10. Test PostgreSQL describe_table
        # =================================================

        result = await registry.execute(
            name="describe_table",
            arguments={
                "table_name": "documents",
            },
        )

        print("\ndescribe_table result:")
        print(result)

    finally:

        # =================================================
        # 11. Close all MCP connections
        # =================================================

        print("\nClosing MCP connections...")

        await filesystem_client.close()

        await github_client.close()

        await postgres_client.close()

        print("All MCP connections closed.")


if __name__ == "__main__":
    asyncio.run(main())
