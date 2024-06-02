"""
Mock requests for testing route
"""
from typing import Any
from unittest.mock import Mock


def mock_response(status_code: int, json_data: dict[str, Any], headers: dict[str, Any] = {}) -> Mock:
    """
    Create mock response for request with status code and json data

    Args:
        status_code (int): status code for mock response
        json_data (dict[str, Any]): json content for mock response
        headers (dict[str, Any], optional): header for the mock response. Defaults to {}.

    Returns:
        Mock: mock response for api
    """

    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    response.headers = headers
    return response


def mock_verify_response(**kwargs) -> Mock:
    """
    Mock response for /verify endpoint call


    Returns:
        Mock: mock response for api
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
        response_headers = {'Allow': 'OPTIONS, GET, HEAD, POST, PUT, PATCH', 'Content-Length': '0'}
        return mock_response(200, None, response_headers)
    elif kwargs["method"] == "head":
        response_headers = {'Content-Type': 'application/json', 'Content-Length': '251'}
        return mock_response(200, None, response_headers)
    elif kwargs["method"] == "post":
        return mock_response(201, {"message": "post request processed"})
    elif kwargs["method"] == "put":
        return mock_response(200, {"message": "put request processed"})
    elif kwargs["method"] == "patch":
        return mock_response(200, {"message": "patch request processed"})
    elif kwargs["method"] == "delete":
        return mock_response(200, {"message": "delete request processed"})


def mock_request_side_effect(url: str, **kwargs) -> Mock:
    """
    Mock API response to test route

    Args:
        url (str): api url

    Returns:
        Mock: mock response of the api
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
