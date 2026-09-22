from src.models import ValidationResult


def validate_json_fields(
    data: dict,
    required_fields: list[str]
) -> list[str]:
    """
    Check whether all required fields exist.
    """

    missing_fields = []

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    return missing_fields


def validate_data_types(
    data: dict,
    expected_types: dict
) -> dict[str, dict[str, str]]:
    """
    Check whether fields contain the expected data types.
    """

    invalid_types = {}

    for field, expected_type in expected_types.items():

        if field not in data:
            continue

        if not isinstance(data[field], expected_type):
            invalid_types[field] = {
                "expected": expected_type.__name__,
                "actual": type(data[field]).__name__
            }

    return invalid_types


def find_unexpected_fields(
    data: dict,
    expected_fields: list[str]
) -> list[str]:
    """
    Find fields that were not explicitly expected.

    Unexpected fields are treated as warnings rather than errors.
    """

    unexpected_fields = []

    for field in data:
        if field not in expected_fields:
            unexpected_fields.append(field)

    return unexpected_fields


def validate_response(
    data: dict,
    expected_fields: list[str],
    expected_types: dict
) -> ValidationResult:
    """
    Perform complete response validation.
    """

    missing_fields = validate_json_fields(
        data,
        expected_fields
    )

    invalid_types = validate_data_types(
        data,
        expected_types
    )

    unexpected_fields = find_unexpected_fields(
        data,
        expected_fields
    )

    is_valid = (
        len(missing_fields) == 0
        and len(invalid_types) == 0
    )

    return ValidationResult(
        valid=is_valid,
        missing_fields=missing_fields,
        invalid_types=invalid_types,
        unexpected_fields=unexpected_fields
    )