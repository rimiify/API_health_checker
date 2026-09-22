from src.database import (
    initialize_database,
    save_health_check
)

from src.history import (
    get_history_summary,
    get_recent_checks
)


def insert_test_data(
    database_path,
    monkeypatch
):

    monkeypatch.setattr(
        "src.database.DATABASE_PATH",
        database_path
    )

    monkeypatch.setattr(
        "src.history.DATABASE_PATH",
        database_path
    )

    initialize_database()

    results = [
        {
            "timestamp": "2026-09-22T10:00:00",
            "name": "Users API",
            "url": "https://example.com/users",
            "status_code": 200,
            "response_time": 0.20,
            "response_size": 100,
            "reachable": True,
            "health": "HEALTHY"
        },
        {
            "timestamp": "2026-09-22T10:01:00",
            "name": "Users API",
            "url": "https://example.com/users",
            "status_code": 200,
            "response_time": 1.50,
            "response_size": 120,
            "reachable": True,
            "health": "DEGRADED"
        },
        {
            "timestamp": "2026-09-22T10:02:00",
            "name": "Posts API",
            "url": "https://example.com/posts",
            "status_code": 500,
            "response_time": 0.30,
            "response_size": 80,
            "reachable": True,
            "health": "UNHEALTHY"
        }
    ]

    for result in results:
        save_health_check(result)


def test_history_summary_all_apis(
    tmp_path,
    monkeypatch
):

    database_path = tmp_path / "test.db"

    insert_test_data(
        database_path,
        monkeypatch
    )

    summary = get_history_summary()

    assert summary["total_checks"] == 3
    assert summary["healthy_checks"] == 1
    assert summary["degraded_checks"] == 1
    assert summary["unhealthy_checks"] == 1


def test_history_summary_specific_api(
    tmp_path,
    monkeypatch
):

    database_path = tmp_path / "test.db"

    insert_test_data(
        database_path,
        monkeypatch
    )

    summary = get_history_summary(
        "Users API"
    )

    assert summary["total_checks"] == 2
    assert summary["healthy_checks"] == 1
    assert summary["degraded_checks"] == 1
    assert summary["unhealthy_checks"] == 0


def test_recent_checks_limit(
    tmp_path,
    monkeypatch
):

    database_path = tmp_path / "test.db"

    insert_test_data(
        database_path,
        monkeypatch
    )

    checks = get_recent_checks(
        limit=2
    )

    assert len(checks) == 2


def test_recent_checks_specific_api(
    tmp_path,
    monkeypatch
):

    database_path = tmp_path / "test.db"

    insert_test_data(
        database_path,
        monkeypatch
    )

    checks = get_recent_checks(
        api_name="Users API",
        limit=10
    )

    assert len(checks) == 2