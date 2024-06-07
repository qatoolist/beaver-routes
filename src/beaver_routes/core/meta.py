from __future__ import annotations

import copy
from typing import Any, Dict, Union, cast

from box import Box

from beaver_routes._types._types import (
    Auth,
    ContentType,
    Cookies,
    DataType,
    FilesType,
    Headers,
    QueryParams,
    Timeout,
)
from beaver_routes.core.httpx_args_handler import HttpxArgsHandler
from beaver_routes.exceptions.exceptions import (
    AttributeNotFoundError,
    InvalidAdditionError,
    InvalidHttpMethodError,
    InvalidHttpxArgumentsError,
    MetaError,
)


class Meta:
    """Class representing metadata for HTTP requests.

    This class encapsulates various metadata attributes for an HTTP request,
    such as query parameters, headers, cookies, authentication, and more.
    It provides methods to convert metadata to `httpx` arguments and to
    manage the metadata attributes.

    Attributes:
        params (QueryParams): Query parameters for the HTTP request.
        headers (Headers): Headers for the HTTP request.
        cookies (Cookies): Cookies for the HTTP request.
        auth (Auth): Authentication information for the HTTP request.
        follow_redirects (Union[bool, None]): Whether to follow redirects.
        timeout (Timeout): Timeout for the HTTP request.
        extensions (Union[Dict[str, Any], None]): Extensions for the HTTP request.
        content (ContentType): Content for the HTTP request.
        data (DataType): Data for the HTTP request.
        files (FilesType): Files for the HTTP request.
        json (Any): JSON data for the HTTP request.

    Methods:
        to_httpx_args(self, method: str) -> Dict[str, Any]:
            Convert the metadata to `httpx` arguments.
        copy(self) -> Meta:
            Create a deep copy of the Meta object.
        to_dict(self) -> Dict[str, Any]:
            Convert the Meta object to a dictionary.
        __add__(self, other: Meta) -> Meta:
            Add two Meta objects together.
    """

    def __init__(
        self,
        *,
        params: QueryParams = None,
        headers: Headers = None,
        cookies: Cookies = None,
        auth: Auth = None,
        follow_redirects: Union[bool, None] = None,
        timeout: Timeout = None,
        extensions: Union[Dict[str, Any], None] = None,
        content: ContentType = None,
        data: DataType = None,
        files: FilesType = None,
        json: Any = None,
    ) -> None:
        """Initialize the Meta object with optional attributes.

        Args:
            params (QueryParams, optional): Query parameters. Defaults to None.
            headers (Headers, optional): Headers. Defaults to None.
            cookies (Cookies, optional): Cookies. Defaults to None.
            auth (Auth, optional): Authentication information. Defaults to None.
            follow_redirects (Union[bool, None], optional): Follow redirects. Defaults to None.
            timeout (Timeout, optional): Timeout. Defaults to None.
            extensions (Union[Dict[str, Any], None], optional): Extensions. Defaults to None.
            content (ContentType, optional): Content. Defaults to None.
            data (DataType, optional): Data. Defaults to None.
            files (FilesType, optional): Files. Defaults to None.
            json (Any, optional): JSON data. Defaults to None.
        """
        self._attributes = Box(default_box=True)
        self._attributes.params = (
            self._wrap(params) if params is not None else Box(default_box=True)
        )
        self._attributes.headers = (
            self._wrap(headers) if headers is not None else Box(default_box=True)
        )
        self._attributes.cookies = (
            self._wrap(cookies) if cookies is not None else Box(default_box=True)
        )
        self._attributes.auth = auth
        self._attributes.follow_redirects = follow_redirects
        self._attributes.timeout = timeout
        self._attributes.extensions = self._wrap(extensions)
        self._attributes.content = (
            content if content is not None else Box(default_box=True)
        )
        self._attributes.data = (
            self._wrap(data) if data is not None else Box(default_box=True)
        )
        self._attributes.files = (
            self._wrap(files) if files is not None else Box(default_box=True)
        )
        self._attributes.json = (
            self._wrap(json) if json is not None else Box(default_box=True)
        )

    def _wrap(self, value: Any) -> Any:
        """Wrap a dictionary value in a Box object.

        Args:
            value (Any): The value to wrap.

        Returns:
            Any: The wrapped value.
        """
        return Box(value, default_box=True) if isinstance(value, dict) else value

    def __getattr__(self, name: str) -> Any:
        """Get an attribute from the Meta object.

        Args:
            name (str): The name of the attribute.

        Returns:
            Any: The value of the attribute.

        Raises:
            AttributeNotFoundError: If the attribute is not found.
        """
        try:
            return getattr(self._attributes, name)
        except AttributeError:
            raise AttributeNotFoundError(f"Attribute '{name}' not found in Meta")

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute in the Meta object.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to set.
        """
        if name == "_attributes":
            super().__setattr__(name, value)
        else:
            setattr(self._attributes, name, self._wrap(value))

    def to_httpx_args(self, method: str) -> Dict[str, Any]:
        """Convert the metadata to `httpx` arguments.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            Dict[str, Any]: The `httpx` arguments.

        Raises:
            InvalidHttpMethodError: If the HTTP method is invalid.
            InvalidHttpxArgumentsError: If the arguments are invalid.
            MetaError: If there is an error converting to `httpx` arguments.
        """
        try:
            return HttpxArgsHandler.convert(self, method)
        except InvalidHttpMethodError as e:
            raise InvalidHttpxArgumentsError(f"Failed to convert to httpx args: {e}")
        except Exception as e:
            raise MetaError(f"Failed to convert to httpx args: {e}")

    def __add__(self, other: Meta) -> Meta:
        """Add two Meta objects together.

        Args:
            other (Meta): The other Meta object.

        Returns:
            Meta: The combined Meta object.

        Raises:
            InvalidAdditionError: If the other object is not a Meta instance.
        """
        if not isinstance(other, Meta):
            raise InvalidAdditionError("Cannot add non-Meta instance.")

        result = Meta()
        for key, value in self._attributes.items():
            if isinstance(value, Box) and isinstance(other._attributes[key], Box):
                result._attributes[key] = value + other._attributes[key]
            else:
                result._attributes[key] = (
                    other._attributes[key]
                    if other._attributes[key] is not None
                    else value
                )
        return result

    def __repr__(self) -> str:
        """Return the string representation of the Meta object.

        Returns:
            str: The string representation of the Meta object.
        """
        return (
            f"Meta(params={self._attributes.params}, headers={self._attributes.headers}, cookies={self._attributes.cookies}, auth={self._attributes.auth}, "
            f"follow_redirects={self._attributes.follow_redirects}, timeout={self._attributes.timeout}, extensions={self._attributes.extensions}, "
            f"content={self._attributes.content}, data={self._attributes.data}, files={self._attributes.files}, json={self._attributes.json})"
        )

    def __str__(self) -> str:
        """Return the string representation of the Meta object.

        Returns:
            str: The formatted string representation of the Meta object.
        """
        return self._dict_to_str(self.to_dict(), indent=4)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Meta object to a dictionary.

        Returns:
            Dict[str, Any]: The dictionary representation of the Meta object.
        """
        return cast(dict[str, Any], self._attributes.to_dict())

    def copy(self) -> Meta:
        """Create a deep copy of the Meta object.

        Returns:
            Meta: The copied Meta object.
        """
        copied_meta = Meta()
        copied_meta._attributes = copy.deepcopy(self._attributes)
        return copied_meta

    @staticmethod
    def _dict_to_str(data: Dict[str, Any], indent: int = 0) -> str:
        """Convert a dictionary to a formatted string.

        Args:
            data (Dict[str, Any]): The dictionary to convert.
            indent (int, optional): The indentation level. Defaults to 0.

        Returns:
            str: The formatted string representation of the dictionary.
        """

        def custom_repr(value: Any | None) -> str | None:
            if value is None:
                return "None"
            elif isinstance(value, dict):
                return Meta._dict_to_str(value, indent=indent + 4)
            return repr(value)

        items = []
        for key, value in data.items():
            items.append(f'{" " * indent}"{key}": {custom_repr(value)}')

        return "{\n" + ",\n".join(items) + "\n" + " " * indent + "}"
