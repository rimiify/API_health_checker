from src.analyzer import analyze_health
from src.models import HealthCheckResult


def test_unreachable_api():
    result = HealthCheckResult(
        url="https://example.com",
        status_code=None,
        response_time=None,
        response_size=None,
        reachable=False,
        json_data=None,
        json_valid=False,
        json_error="No response received"
    )

    health = analyze_health(result)

    assert health == "UNHEALTHY"


def test_server_error():
    result = HealthCheckResult(
        url="https://example.com",
        status_code=500,
        response_time=0.5,
        response_size=100,
        reachable=True,
        json_data={},
        json_valid=True,
        json_error=None
    )

    health = analyze_health(result)

    assert health == "UNHEALTHY"


def test_client_error():
    result = HealthCheckResult(
        url="https://example.com",
        status_code=404,
        response_time=0.5,
        response_size=100,
        reachable=True,
        json_data={},
        json_valid=True,
        json_error=None
    )

    health = analyze_health(result)

    assert health == "DEGRADED"


def test_slow_response():
    result = HealthCheckResult(
        url="https://example.com",
        status_code=200,
        response_time=2.5,
        response_size=100,
        reachable=True,
        json_data={},
        json_valid=True,
        json_error=None
    )

    health = analyze_health(result)

    assert health == "DEGRADED"


def test_healthy_api():
    result = HealthCheckResult(
        url="https://example.com",
        status_code=200,
        response_time=0.5,
        response_size=100,
        reachable=True,
        json_data={},
        json_valid=True,
        json_error=None
    )

    health = analyze_health(result)

    assert health == "HEALTHY"