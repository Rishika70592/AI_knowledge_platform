from sqlalchemy import create_engine, text

from app.core.config import DATABASE_URL


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured."
    )


sync_database_url = DATABASE_URL.replace(
    "postgresql+asyncpg://",
    "postgresql://",
)

engine = create_engine(
    sync_database_url,
)


def main():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        print(
            "PostgreSQL connection:",
            result.scalar(),
        )

        result = connection.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
        )

        print("\nTables:")

        for row in result:
            print("-", row[0])


if __name__ == "__main__":
    main()
