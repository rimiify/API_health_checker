from src.models import HealthCheckResult


def analyze_health(
    result: HealthCheckResult,
    max_response_time: float = 2.0
) -> str:
    """
    Determine the health status of an API.

    Args:
        result (HealthCheckResult): API health check result.
        max_response_time (float): Maximum acceptable response time.

    Returns:
        str: HEALTHY, DEGRADED, or UNHEALTHY.
    """

    if not result.reachable:
        return "UNHEALTHY"

    if result.status_code >= 500:
        return "UNHEALTHY"

    if result.status_code >= 400:
        return "DEGRADED"

    if result.response_time > max_response_time:
        return "DEGRADED"

    return "HEALTHY"