import requests

from src.api_client import make_request


class MockResponse:
    pass


def test_successful_request(monkeypatch):

    mock_response = MockResponse()
    mock_response.status_code = 200

    def mock_get(url, timeout):
        return mock_response

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    response = make_request(
        "https://example.com"
    )

    assert response.status_code == 200
def test_request_timeout(monkeypatch):

    def mock_get(url, timeout):
        raise requests.Timeout()

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    response = make_request(
        "https://example.com"
    )

    assert response is None
def test_connection_error(monkeypatch):

    def mock_get(url, timeout):
        raise requests.ConnectionError()

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    response = make_request(
        "https://example.com"
    )

    assert response is None
def test_general_request_error(monkeypatch):

    def mock_get(url, timeout):
        raise requests.RequestException(
            "Something went wrong"
        )

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    response = make_request(
        "https://example.com"
    )

    assert response is None
