from dataclasses import dataclass
from typing import Any


@dataclass
class HealthCheckResult:
    """
    Represents the result of checking an API endpoint.
    """

    url: str
    status_code: int | None
    response_time: float | None
    response_size: int | None
    reachable: bool
    json_data: dict[str, Any] | None
    json_valid: bool
    json_error: str | None


@dataclass
class ValidationResult:
    """
    Represents the result of validating an API response.
    """

    valid: bool
    missing_fields: list[str]
    invalid_types: dict[str, dict[str, str]]
    unexpected_fields: list[str]


@dataclass
class MonitoringRecord:
    """
    Represents a completed API monitoring check.
    """

    name: str
    timestamp: str
    url: str
    status_code: int | None
    response_time: float | None
    response_size: int | None
    reachable: bool
    health: str