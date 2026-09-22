import sqlite3
from pathlib import Path
from typing import Any


DATABASE_PATH = Path("data/api_health.db")


def initialize_database() -> None:
    """
    Create the database and health_checks table if they
    do not already exist.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS health_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                api_name TEXT NOT NULL,
                url TEXT NOT NULL,
                status_code INTEGER,
                response_time REAL,
                reachable INTEGER NOT NULL,
                health TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def save_health_check(
    result: dict[str, Any]
) -> None:
    """
    Save one API health check result to SQLite.

    Args:
        result: Monitoring result converted to a dictionary.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        connection.execute(
            """
            INSERT INTO health_checks (
                timestamp,
                api_name,
                url,
                status_code,
                response_time,
                reachable,
                health
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result["timestamp"],
                result["name"],
                result["url"],
                result["status_code"],
                result["response_time"],
                int(result["reachable"]),
                result["health"]
            )
        )

        connection.commit()

    finally:
        connection.close()