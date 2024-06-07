from typing import Any

import httpx

from beaver_routes.core.response import Response


class RequestHandler:
    """Handler class for making HTTP requests.

    This class provides static methods to make synchronous and asynchronous HTTP requests
    using the httpx library. It abstracts the httpx.Client and httpx.AsyncClient usage.

    Methods:
        sync_request(method: str, url: str, **kwargs: Any) -> Response:
            Make a synchronous HTTP request.
        async_request(method: str, url: str, **kwargs: Any) -> Response:
            Make an asynchronous HTTP request.
    """

    @staticmethod
    def sync_request(method: str, url: str, **kwargs: Any) -> Response:
        """Make a synchronous HTTP request.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL for the request.
            **kwargs (Any): Additional arguments to pass to the httpx.Client request method.

        Returns:
            Response: The HTTP response.

        Example:
            >>> response = RequestHandler.sync_request("GET", "http://example.com")
            >>> print(response.status_code)
        """
        with httpx.Client() as client:
            return Response(client.request(method=method, url=url, **kwargs))

    @staticmethod
    async def async_request(method: str, url: str, **kwargs: Any) -> Response:
        """Make an asynchronous HTTP request.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL for the request.
            **kwargs (Any): Additional arguments to pass to the httpx.AsyncClient request method.

        Returns:
            Response: The HTTP response.

        Example:
            >>> response = await RequestHandler.async_request("GET", "http://example.com")
            >>> print(response.status_code)
        """
        async with httpx.AsyncClient() as client:
            response: Any = await client.request(method=method, url=url, **kwargs)
            return Response(response)
