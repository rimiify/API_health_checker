import requests


def make_request(
    url: str,
    timeout: int = 5
) -> requests.Response | None:
    """
    Send a GET request to an API endpoint.

    Args:
        url: API endpoint URL.
        timeout: Maximum time to wait for a response.

    Returns:
        API response if successful, otherwise None.
    """

    try:
        response = requests.get(
            url,
            timeout=timeout
        )

        return response

    except requests.Timeout:
        print(f"Request timed out: {url}")

    except requests.ConnectionError:
        print(f"Could not connect to: {url}")

    except requests.RequestException as error:
        print(f"Request failed: {error}")

    return None