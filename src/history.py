import sqlite3
from typing import Any

from src.database import DATABASE_PATH


def get_history_summary(
    api_name: str | None = None
) -> dict[str, Any]:
    """
    Get summary statistics from API health history.

    Args:
        api_name: Optional API name to filter by.

    Returns:
        Dictionary containing historical statistics.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        query = """
            SELECT
                COUNT(*),
                AVG(response_time),
                MAX(response_time),
                SUM(
                    CASE
                        WHEN health = 'UNHEALTHY'
                        THEN 1
                        ELSE 0
                    END
                ),
                SUM(
                    CASE
                        WHEN health = 'HEALTHY'
                        THEN 1
                        ELSE 0
                    END
                ),
                SUM(
                    CASE
                        WHEN health = 'DEGRADED'
                        THEN 1
                        ELSE 0
                    END
                )
            FROM health_checks
        """

        parameters = ()

        if api_name:
            query += " WHERE api_name = ?"
            parameters = (api_name,)

        row = connection.execute(
            query,
            parameters
        ).fetchone()

        return {
            "total_checks": row[0],
            "average_response_time": row[1],
            "slowest_response": row[2],
            "unhealthy_checks": row[3],
            "healthy_checks": row[4],
            "degraded_checks": row[5]
        }

    finally:
        connection.close()


def get_recent_checks(
    api_name: str | None = None,
    limit: int = 10
) -> list[tuple[Any, ...]]:
    """
    Get the most recent API health checks.

    Args:
        api_name: Optional API name to filter by.
        limit: Maximum number of records to return.

    Returns:
        List of historical health check records.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        if api_name:

            query = """
                SELECT
                    timestamp,
                    status_code,
                    response_time,
                    health,
                    reachable
                FROM health_checks
                WHERE api_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """

            return connection.execute(
                query,
                (api_name, limit)
            ).fetchall()

        query = """
            SELECT
                timestamp,
                api_name,
                status_code,
                response_time,
                health,
                reachable
            FROM health_checks
            ORDER BY timestamp DESC
            LIMIT ?
        """

        return connection.execute(
            query,
            (limit,)
        ).fetchall()

    finally:
        connection.close()