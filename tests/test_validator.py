from src.validator import (
    validate_json_fields,
    validate_data_types,
    find_unexpected_fields,
    validate_response
)


def test_validate_json_fields():
    data = {
        "id": 1,
        "name": "John",
        "email": "john@example.com"
    }

    required_fields = ["id", "name", "email"]

    missing_fields = validate_json_fields(
        data,
        required_fields
    )

    assert missing_fields == []


def test_missing_json_field():
    data = {
        "id": 1,
        "name": "John"
    }

    required_fields = ["id", "name", "email"]

    missing_fields = validate_json_fields(
        data,
        required_fields
    )

    assert missing_fields == ["email"]


def test_validate_data_types():
    data = {
        "id": 1,
        "name": "John"
    }

    expected_types = {
        "id": int,
        "name": str
    }

    invalid_types = validate_data_types(
        data,
        expected_types
    )

    assert invalid_types == {}


def test_invalid_data_type():
    data = {
        "id": "1",
        "name": "John"
    }

    expected_types = {
        "id": int,
        "name": str
    }

    invalid_types = validate_data_types(
        data,
        expected_types
    )

    assert "id" in invalid_types
    assert invalid_types["id"]["expected"] == "int"
    assert invalid_types["id"]["actual"] == "str"


def test_unexpected_fields():
    data = {
        "id": 1,
        "name": "John",
        "email": "john@example.com",
        "age": 20
    }

    expected_fields = ["id", "name", "email"]

    unexpected_fields = find_unexpected_fields(
        data,
        expected_fields
    )

    assert unexpected_fields == ["age"]


def test_complete_valid_response():
    data = {
        "id": 1,
        "name": "John",
        "email": "john@example.com"
    }

    expected_fields = [
        "id",
        "name",
        "email"
    ]

    expected_types = {
        "id": int,
        "name": str,
        "email": str
    }

    result = validate_response(
        data,
        expected_fields,
        expected_types
    )

    assert result.valid is True
    assert result.missing_fields == []
    assert result.invalid_types == {}


def test_complete_invalid_response():
    data = {
        "id": "1",
        "name": "John"
    }

    expected_fields = [
        "id",
        "name",
        "email"
    ]

    expected_types = {
        "id": int,
        "name": str,
        "email": str
    }

    result = validate_response(
        data,
        expected_fields,
        expected_types
    )

    assert result.valid is False
    assert result.missing_fields == ["email"]
    assert "id" in result.invalid_types