from src.database import (
    initialize_database,
    save_health_check
)


def test_initialize_database(tmp_path, monkeypatch):

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.database.DATABASE_PATH",
        database_path
    )

    initialize_database()

    assert database_path.exists()


def test_save_health_check(tmp_path, monkeypatch):

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.database.DATABASE_PATH",
        database_path
    )

    initialize_database()

    result = {
        "timestamp": "2026-09-22T12:00:00",
        "name": "Test API",
        "url": "https://example.com",
        "status_code": 200,
        "response_time": 0.25,
        "response_size": 120,
        "reachable": True,
        "health": "HEALTHY"
    }

    save_health_check(result)

    import sqlite3

    connection = sqlite3.connect(
        database_path
    )

    row = connection.execute(
        """
        SELECT
            api_name,
            status_code,
            response_time,
            health
        FROM health_checks
        """
    ).fetchone()

    connection.close()

    assert row == (
        "Test API",
        200,
        0.25,
        "HEALTHY"
    )


def test_save_unreachable_api(tmp_path, monkeypatch):

    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.database.DATABASE_PATH",
        database_path
    )

    initialize_database()

    result = {
        "timestamp": "2026-09-22T12:00:00",
        "name": "Broken API",
        "url": "https://broken.example.com",
        "status_code": None,
        "response_time": None,
        "response_size": None,
        "reachable": False,
        "health": "UNHEALTHY"
    }

    save_health_check(result)

    import sqlite3

    connection = sqlite3.connect(
        database_path
    )

    row = connection.execute(
        """
        SELECT
            reachable,
            health
        FROM health_checks
        """
    ).fetchone()

    connection.close()

    assert row == (
        0,
        "UNHEALTHY"
    )