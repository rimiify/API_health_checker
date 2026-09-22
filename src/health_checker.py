from src.api_client import make_request
from src.models import HealthCheckResult


def check_api(url: str) -> HealthCheckResult:
    """
    Check the health of an API endpoint.

    Args:
        url (str): API endpoint URL.

    Returns:
        HealthCheckResult: Result of the API health check.
    """

    response = make_request(url)

    if response is None:
        return HealthCheckResult(
            url=url,
            status_code=None,
            response_time=None,
            response_size=None,
            reachable=False,
            json_data=None,
            json_valid=False,
            json_error="No response received"
        )

    try:
        json_data = response.json()

        return HealthCheckResult(
            url=url,
            status_code=response.status_code,
            response_time=response.elapsed.total_seconds(),
            response_size=len(response.content),
            reachable=True,
            json_data=json_data,
            json_valid=True,
            json_error=None
        )

    except ValueError:
        return HealthCheckResult(
            url=url,
            status_code=response.status_code,
            response_time=response.elapsed.total_seconds(),
            response_size=len(response.content),
            reachable=True,
            json_data=None,
            json_valid=False,
            json_error="Response is not valid JSON"
        )