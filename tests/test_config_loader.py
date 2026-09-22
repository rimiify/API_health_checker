import json

import pytest

from src.config_loader import load_endpoints


def create_config(
    tmp_path,
    config
):
    file_path = tmp_path / "endpoints.json"

    with file_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file
        )

    return file_path


def test_load_valid_config(tmp_path):

    config = {
        "endpoints": [
            {
                "name": "Test API",
                "url": "https://example.com",
                "expected_fields": ["id"],
                "expected_types": {
                    "id": "int"
                }
            }
        ]
    }

    path = create_config(
        tmp_path,
        config
    )

    endpoints = load_endpoints(path)

    assert len(endpoints) == 1
    assert endpoints[0]["name"] == "Test API"
    assert endpoints[0]["expected_types"]["id"] is int


def test_missing_endpoints_key(tmp_path):

    config = {}

    path = create_config(
        tmp_path,
        config
    )

    with pytest.raises(
        ValueError,
        match="endpoints"
    ):
        load_endpoints(path)


def test_empty_endpoints_list(tmp_path):

    config = {
        "endpoints": []
    }

    path = create_config(
        tmp_path,
        config
    )

    with pytest.raises(
        ValueError,
        match="At least one endpoint"
    ):
        load_endpoints(path)


def test_missing_url(tmp_path):

    config = {
        "endpoints": [
            {
                "name": "Test API"
            }
        ]
    }

    path = create_config(
        tmp_path,
        config
    )

    with pytest.raises(
        ValueError,
        match="url"
    ):
        load_endpoints(path)


def test_invalid_response_time(tmp_path):

    config = {
        "endpoints": [
            {
                "name": "Test API",
                "url": "https://example.com",
                "max_response_time": "fast"
            }
        ]
    }

    path = create_config(
        tmp_path,
        config
    )

    with pytest.raises(
        ValueError,
        match="max_response_time"
    ):
        load_endpoints(path)


def test_invalid_data_type(tmp_path):

    config = {
        "endpoints": [
            {
                "name": "Test API",
                "url": "https://example.com",
                "expected_types": {
                    "id": "banana"
                }
            }
        ]
    }

    path = create_config(
        tmp_path,
        config
    )

    with pytest.raises(
        ValueError,
        match="Unsupported data type"
    ):
        load_endpoints(path)


def test_negative_response_time(tmp_path):

    config = {
        "endpoints": [
            {
                "name": "Test API",
                "url": "https://example.com",
                "max_response_time": -1
            }
        ]
    }

    path = create_config(
        tmp_path,
        config
    )

    with pytest.raises(
        ValueError,
        match="greater than 0"
    ):
        load_endpoints(path)