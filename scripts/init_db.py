import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = (
    PROJECT_ROOT
    / "sql"
    / "schema.sql"
)


def main() -> None:

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    schema_sql = SCHEMA_PATH.read_text(
        encoding="utf-8"
    )

    statements = [
        statement.strip()
        for statement in schema_sql.split(";")
        if statement.strip()
    ]

    with psycopg.connect(database_url) as conn:

        for statement in statements:
            conn.execute(statement)

        conn.commit()

    print("Database schema initialized successfully.")


if __name__ == "__main__":
    main()