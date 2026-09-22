import json
from datetime import datetime
from pathlib import Path

from src.models import HealthCheckResult, ValidationResult


def print_api_report(
    result: HealthCheckResult,
    health: str,
    validation: ValidationResult | None = None,
    name: str | None = None
) -> None:
    """
    Print a formatted health report for one API.
    """

    print("\n========================================")

    if name:
        print(f"API: {name}")

    print("========================================")

    print(f"URL            : {result.url}")
    print(f"Status Code    : {result.status_code}")
    print(f"Response Time  : {result.response_time} seconds")
    print(f"Response Size  : {result.response_size} bytes")
    print(f"Reachable      : {result.reachable}")
    print(f"Health         : {health}")

    if validation is not None:

        print("\nResponse Validation")
        print("-------------------")

        print(f"Valid          : {validation.valid}")
        print(f"Missing Fields : {validation.missing_fields}")
        print(f"Invalid Types  : {validation.invalid_types}")
        print(f"Unexpected     : {validation.unexpected_fields}")


def save_json_report(results: list[dict]) -> None:
    """
    Save API health results and summary to a JSON file.

    Args:
        results: List of API health check results.
    """

    report_path = Path(
        "reports/health_report.json"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    total = len(results)

    healthy = sum(
        1
        for result in results
        if result["health"] == "HEALTHY"
    )

    degraded = sum(
        1
        for result in results
        if result["health"] == "DEGRADED"
    )

    unhealthy = sum(
        1
        for result in results
        if result["health"] == "UNHEALTHY"
    )

    report = {
        "generated_at": datetime.now().isoformat(),

        "summary": {
            "total": total,
            "healthy": healthy,
            "degraded": degraded,
            "unhealthy": unhealthy
        },

        "apis": results
    }

    with report_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )


def print_history_summary(
    summary: dict,
    api_name: str | None = None
) -> None:
    """
    Print historical monitoring statistics.
    """

    print("\n========================================")

    if api_name:
        print(f"History: {api_name}")
    else:
        print("History: All APIs")

    print("========================================")

    print(
        f"Total Checks          : "
        f"{summary['total_checks']}"
    )

    print(
        f"Average Response Time : "
        f"{summary['average_response_time']}"
    )

    print(
        f"Slowest Response      : "
        f"{summary['slowest_response']}"
    )

    print(
        f"Healthy Checks        : "
        f"{summary['healthy_checks']}"
    )

    print(
        f"Degraded Checks       : "
        f"{summary['degraded_checks']}"
    )

    print(
        f"Unhealthy Checks      : "
        f"{summary['unhealthy_checks']}"
    )


def print_recent_checks(
    checks,
    api_name: str | None = None
) -> None:
    """
    Print the most recent health checks.
    """

    print("\n========================================")

    if api_name:
        print(f"Recent Checks: {api_name}")
    else:
        print("Recent Checks: All APIs")

    print("========================================")

    if not checks:
        print("No historical checks found.")
        return

    for check in checks:

        print("\n-------------------")

        if api_name:
            (
                timestamp,
                status_code,
                response_time,
                health,
                reachable
            ) = check

            print(f"Time          : {timestamp}")
            print(f"Status Code   : {status_code}")
            print(f"Response Time : {response_time}")
            print(f"Health        : {health}")
            print(f"Reachable     : {bool(reachable)}")

        else:
            (
                timestamp,
                name,
                status_code,
                response_time,
                health,
                reachable
            ) = check

            print(f"API           : {name}")
            print(f"Time          : {timestamp}")
            print(f"Status Code   : {status_code}")
            print(f"Response Time : {response_time}")
            print(f"Health        : {health}")
            print(f"Reachable     : {bool(reachable)}")