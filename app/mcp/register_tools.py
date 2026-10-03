from app.mcp.client import MCPClient
from app.mcp.tool_adapter import MCPToolAdapter
from app.agents.tools import ToolRegistry


async def register_filesystem_tools(
    tool_registry: ToolRegistry,
    client: MCPClient,
):
    tools = await client.list_tools()

    for tool in tools:

        adapter = MCPToolAdapter(
            client=client,
            tool_name=tool.name,
        )

        tool_registry.register(
            name=tool.name,
            description=tool.description or "",
            parameters=tool.input_schema,

            function=adapter.execute,
        )
