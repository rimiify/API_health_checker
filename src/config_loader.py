import json
from pathlib import Path
from typing import Any


TYPE_MAP: dict[str, type] = {
    "int": int,
    "str": str,
    "float": float,
    "bool": bool
}


def validate_endpoint_config(
    endpoint: dict[str, Any]
) -> None:
    """
    Validate a single API endpoint configuration.

    Raises:
        ValueError: If the configuration is invalid.
    """

    required_fields = [
        "name",
        "url"
    ]

    for field in required_fields:

        if field not in endpoint:
            raise ValueError(
                f"Missing required field: '{field}'"
            )

    if not isinstance(endpoint["name"], str):
        raise ValueError(
            "'name' must be a string"
        )

    if not endpoint["name"].strip():
        raise ValueError(
            "'name' cannot be empty"
        )

    if not isinstance(endpoint["url"], str):
        raise ValueError(
            "'url' must be a string"
        )

    if not endpoint["url"].strip():
        raise ValueError(
            "'url' cannot be empty"
        )

    max_response_time = endpoint.get(
        "max_response_time",
        2.0
    )

    if not isinstance(
        max_response_time,
        (int, float)
    ):
        raise ValueError(
            "'max_response_time' must be a number"
        )

    if max_response_time <= 0:
        raise ValueError(
            "'max_response_time' must be greater than 0"
        )

    expected_fields = endpoint.get(
        "expected_fields",
        []
    )

    if not isinstance(
        expected_fields,
        list
    ):
        raise ValueError(
            "'expected_fields' must be a list"
        )

    expected_types = endpoint.get(
        "expected_types",
        {}
    )

    if not isinstance(
        expected_types,
        dict
    ):
        raise ValueError(
            "'expected_types' must be an object"
        )

    for field, data_type in expected_types.items():

        if data_type not in TYPE_MAP:
            raise ValueError(
                f"Unsupported data type "
                f"'{data_type}' for field '{field}'"
            )


def load_endpoints(
    config_path: str | Path
) -> list[dict[str, Any]]:
    """
    Load and validate API endpoint configuration.

    Args:
        config_path: Path to the configuration file.

    Returns:
        List of validated API endpoint configurations.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration is invalid.
        json.JSONDecodeError: If the JSON is malformed.
    """

    path = Path(config_path)

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

    if "endpoints" not in config:
        raise ValueError(
            "Configuration must contain "
            "'endpoints'"
        )

    endpoints = config["endpoints"]

    if not isinstance(endpoints, list):
        raise ValueError(
            "'endpoints' must be a list"
        )

    if not endpoints:
        raise ValueError(
            "At least one endpoint must be configured"
        )

    for endpoint in endpoints:

        if not isinstance(endpoint, dict):
            raise ValueError(
                "Each endpoint must be an object"
            )

        validate_endpoint_config(endpoint)

        expected_types = endpoint.get(
            "expected_types",
            {}
        )

        converted_types = {}

        for field, data_type in expected_types.items():

            converted_types[field] = TYPE_MAP[
                data_type
            ]

        endpoint["expected_types"] = converted_types

    return endpoints