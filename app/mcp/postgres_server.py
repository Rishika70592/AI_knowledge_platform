from sqlalchemy import create_engine, text
from mcp.server.mcpserver import MCPServer

from app.core.config import DATABASE_URL


mcp = MCPServer("PostgreSQL Server")

@mcp.resource("schema://database")
def database_schema() -> str:
    """Return a summary of the PostgreSQL database schema."""

    query = text("""
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).fetchall()

    lines = []

    current_table = None

    for row in rows:
        table_name = row[0]
        column_name = row[1]
        data_type = row[2]

        if table_name != current_table:
            lines.append(f"\nTable: {table_name}")
            current_table = table_name

        lines.append(
            f"  - {column_name}: {data_type}"
        )

    return "\n".join(lines)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

sync_database_url = DATABASE_URL.replace(
    "postgresql+asyncpg://",
    "postgresql://"
)

engine = create_engine(sync_database_url)



@mcp.tool()
def list_tables() -> list[str]:
    """List all tables in the public PostgreSQL schema."""

    query = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).fetchall()

    return [row[0] for row in rows]


@mcp.tool()
def describe_table(table_name: str) -> list[dict]:
    """Return column information for a table."""

    query = text("""
        SELECT
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = :table_name
        ORDER BY ordinal_position
    """)

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            {"table_name": table_name}
        ).mappings().all()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run()

