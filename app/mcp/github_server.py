import httpx

from mcp.server.mcpserver import MCPServer


mcp = MCPServer("GitHub Server")


@mcp.tool()
async def search_repositories(query: str) -> list[dict]:
    """Search public GitHub repositories."""

    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": 5,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers={
                "Accept": "application/vnd.github+json"
            },
        )

    response.raise_for_status()

    data = response.json()

    return [
        {
            "name": repo["full_name"],
            "description": repo["description"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
        }
        for repo in data["items"]
    ]


@mcp.tool()
async def get_repository(owner: str, repo: str) -> dict:
    """Get information about a public GitHub repository."""

    url = f"https://api.github.com/repos/{owner}/{repo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Accept": "application/vnd.github+json"
            },
        )

    response.raise_for_status()

    data = response.json()

    return {
        "name": data["full_name"],
        "description": data["description"],
        "url": data["html_url"],
        "stars": data["stargazers_count"],
        "language": data["language"],
        "forks": data["forks_count"],
    }


if __name__ == "__main__":
    mcp.run()
