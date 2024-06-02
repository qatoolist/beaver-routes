"""
Mock requests for testing route
"""

from typing import Any, Dict, Optional
from unittest.mock import Mock


def mock_response(
    status_code: int,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
) -> Mock:
    """
    Create mock response for request with status code and json data.

    Args:
        status_code (int): Status code for mock response.
        json_data (Optional[Dict[str, Any]]): JSON content for mock response.
        headers (Optional[Dict[str, Any]]): Headers for the mock response. Defaults to None.

    Returns:
        Mock: Mock response for API.
    """

    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    response.headers = headers or {}
    return response


def mock_verify_response(**kwargs: Any) -> Mock:
    """
    Mock response for /verify endpoint call.

    Returns:
        Mock: Mock response for API.
    """
    if kwargs["method"] == "get":
        if "key" in kwargs.get("params", {}):
            if isinstance(kwargs["params"]["key"], int):
                return mock_response(200, {"message": "valid key"})
            else:
                return mock_response(400, {"message": "bad key"})
        else:
            return mock_response(400, {"message": "missing parameter key"})
    elif kwargs["method"] == "options":
        response_headers = {
            "Allow": "OPTIONS, GET, HEAD, POST, PUT, PATCH",
            "Content-Length": "0",
        }
        return mock_response(200, None, response_headers)
    elif kwargs["method"] == "head":
        response_headers = {"Content-Type": "application/json", "Content-Length": "251"}
        return mock_response(200, None, response_headers)
    elif kwargs["method"] == "post":
        return mock_response(201, {"message": "post request processed"})
    elif kwargs["method"] == "put":
        return mock_response(200, {"message": "put request processed"})
    elif kwargs["method"] == "patch":
        return mock_response(200, {"message": "patch request processed"})
    elif kwargs["method"] == "delete":
        return mock_response(200, {"message": "delete request processed"})
    else:
        return mock_response(405, {"message": "method not allowed"})


def mock_request_side_effect(url: str, **kwargs: Any) -> Mock:
    """
    Mock API response to test route.

    Args:
        url (str): API URL.

    Returns:
        Mock: Mock response of the API.
    """
    if url.endswith("/verify"):
        return mock_verify_response(**kwargs)
    elif url.endswith("/pong"):
        response = Mock()
        response.status_code = 200
        response.json.return_value = kwargs
        return response
    else:
        return mock_response(404, {"message": "url not found"})
