from app.agents.tools import ToolRegistry

from app.mcp.client import MCPClient
from app.mcp.register_tools import register_filesystem_tools


async def create_mcp_registry():

    registry = ToolRegistry()

    filesystem_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.filesystem_server",
        ],
    )

    await filesystem_client.connect()

    await register_filesystem_tools(
        tool_registry=registry,
        client=filesystem_client,
    )

    return registry, [
        filesystem_client,
    ]
