from pathlib import Path

from mcp.server.mcpserver import MCPServer


mcp = MCPServer("Filesystem Server")


@mcp.tool()
def read_file(path: str) -> str:
    """Read a text file."""
    file_path = Path(path)

    if not file_path.exists():
        return f"File not found: {path}"

    if not file_path.is_file():
        return f"Not a file: {path}"

    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def list_files(directory: str) -> list[str]:
    """List files in a directory."""
    directory_path = Path(directory)

    if not directory_path.exists():
        return [f"Directory not found: {directory}"]

    if not directory_path.is_dir():
        return [f"Not a directory: {directory}"]

    return [
        str(path)
        for path in directory_path.iterdir()
        if path.is_file()
    ]


if __name__ == "__main__":
    mcp.run()
