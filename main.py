import argparse
from dataclasses import asdict
from datetime import datetime

from src.analyzer import analyze_health
from src.config_loader import load_endpoints
from src.database import initialize_database, save_health_check
from src.health_checker import check_api
from src.history import get_history_summary, get_recent_checks
from src.logger import setup_logger
from src.models import MonitoringRecord
from src.reporter import (
    print_api_report,
    print_history_summary,
    print_recent_checks,
    save_json_report,
)
from src.validator import validate_response


CONFIG_PATH = "config/endpoints.json"


def run_health_check(endpoints):
    """
    Run health checks for the selected API endpoints.
    """

    logger = setup_logger()

    results = []

    for endpoint in endpoints:

        name = endpoint["name"]
        url = endpoint["url"]

        logger.info(
            f"Starting health check for {name}: {url}"
        )

        # Check API
        result = check_api(url)

        # Analyze health
        health = analyze_health(
            result,
            endpoint.get("max_response_time", 2.0)
        )

        # Validate JSON response
        validation = None

        if result.json_valid and isinstance(
            result.json_data,
            dict
        ):
            validation = validate_response(
                result.json_data,
                endpoint.get("expected_fields", []),
                endpoint.get("expected_types", {})
            )

        # Print report
        print_api_report(
            result,
            health,
            validation,
            name
        )

        # Create monitoring record
        record = MonitoringRecord(
            name=name,
            timestamp=datetime.now().isoformat(),
            url=result.url,
            status_code=result.status_code,
            response_time=result.response_time,
            response_size=result.response_size,
            reachable=result.reachable,
            health=health
        )

        # Save to database
        save_health_check(
            asdict(record)
        )

        # Add result to JSON report
        report_result = asdict(record)

        if validation is not None:
            report_result["validation"] = asdict(
                validation
            )

        results.append(report_result)

        logger.info(
            f"Completed health check for {name}: {health}"
        )

    save_json_report(results)

    print("\nHealth report saved to:")
    print("reports/health_report.json")


def parse_arguments():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description="API Health Checker"
    )

    mode_group = parser.add_mutually_exclusive_group(
        required=True
    )

    mode_group.add_argument(
        "--all",
        action="store_true",
        help="Check all configured APIs"
    )

    mode_group.add_argument(
        "--history",
        action="store_true",
        help="Show historical monitoring statistics"
    )

    parser.add_argument(
        "--endpoint",
        type=str,
        help="Target a specific API by name"
    )

    parser.add_argument(
        "--recent",
        type=int,
        metavar="N",
        help="Show the N most recent checks"
    )

    return parser.parse_args()


def main():
    """
    Main application entry point.
    """

    initialize_database()

    args = parse_arguments()

    # -----------------------------
    # HISTORY MODE
    # -----------------------------

    if args.history:

        summary = get_history_summary(
            args.endpoint
        )

        print_history_summary(
            summary,
            args.endpoint
        )

        if args.recent:

            recent_checks = get_recent_checks(
                args.endpoint,
                args.recent
            )

            print_recent_checks(
                recent_checks,
                args.endpoint
            )

        return

    # -----------------------------
    # HEALTH CHECK MODE
    # -----------------------------

    endpoints = load_endpoints(
        CONFIG_PATH
    )

    if args.all:

        selected_endpoints = endpoints

    else:

        selected_endpoints = [
            endpoint
            for endpoint in endpoints
            if endpoint["name"] == args.endpoint
        ]

        if not selected_endpoints:

            print(
                f"Endpoint not found: {args.endpoint}"
            )

            return

    run_health_check(
        selected_endpoints
    )


if __name__ == "__main__":
    main()