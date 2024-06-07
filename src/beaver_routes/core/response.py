from typing import Any


class Response:
    """
    A class representing an HTTP response within the beaver-routes DSL.

    This class provides all features of an HTTP response while maintaining a consistent
    interface for beaver-routes.

    Attributes:
        response (Any): The actual HTTP response object.
        status_code (int): The HTTP status code of the response.
        headers (dict[str, str]): The headers of the response.
        cookies (dict[str, str]): The cookies of the response.
        url (str): The URL of the response.
        content (bytes): The byte content of the response.
        text (str): The text content of the response.
    """

    def __init__(self, response: Any) -> None:
        """
        Initialize the Response with an HTTP response object.

        Args:
            response (Any): The actual HTTP response object.
        """
        self._response = response

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the actual response object.

        Args:
            name (str): The name of the attribute to access.

        Returns:
            Any: The value of the attribute.
        """
        return getattr(self._response, name)

    @property
    def json_content(self) -> Any:
        """
        Return the JSON content of the response.

        Returns:
            Any: The JSON content of the response.
        """
        return self._response.json()

    @property
    def text(self) -> str:
        """
        Return the text content of the response.

        Returns:
            str: The text content of the response.
        """
        return str(self._response.text)

    @property
    def content(self) -> bytes:
        """
        Return the byte content of the response.

        Returns:
            bytes: The byte content of the response.
        """
        return bytes(self._response.content)

    @property
    def status_code(self) -> int:
        """
        Return the HTTP status code of the response.

        Returns:
            int: The HTTP status code of the response.
        """
        return int(self._response.status_code)

    @property
    def headers(self) -> dict[str, str]:
        """
        Return the headers of the response.

        Returns:
            dict[str, str]: The headers of the response.
        """
        return dict(self._response.headers)

    @property
    def cookies(self) -> dict[str, str]:
        """
        Return the cookies of the response.

        Returns:
            dict[str, str]: The cookies of the response.
        """
        return dict(self._response.cookies)

    @property
    def url(self) -> str:
        """
        Return the URL of the response.

        Returns:
            str: The URL of the response.
        """
        return str(self._response.url)
