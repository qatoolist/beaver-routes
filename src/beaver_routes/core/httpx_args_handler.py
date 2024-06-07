from typing import Any, Dict

from box import Box

from beaver_routes.exceptions.exceptions import (
    InvalidHttpMethodError,
    InvalidHttpxArgumentsError,
)


class HttpxArgsHandler:
    """Handler for converting Meta objects to httpx-compatible arguments.

    This class provides methods to convert Meta objects to dictionaries
    compatible with the httpx library for making HTTP requests. It ensures
    that the arguments are correctly formatted based on the HTTP method used.

    Methods:
        convert(meta: Any, method: str) -> Dict[str, Any]:
            Convert the Meta object to httpx arguments based on the HTTP method.
    """

    @staticmethod
    def convert(meta: Any, method: str) -> Dict[str, Any]:
        """Convert the Meta object to httpx arguments based on the HTTP method.

        Args:
            meta (Any): The Meta object containing request metadata.
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            Dict[str, Any]: The httpx-compatible arguments.

        Raises:
            InvalidHttpMethodError: If the HTTP method is invalid.
            InvalidHttpxArgumentsError: If there is an error in the arguments.
        """
        valid_methods = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
        if method not in valid_methods:
            raise InvalidHttpMethodError(f"Invalid HTTP method: {method}")

        try:
            args = HttpxArgsHandler._build_common_args(meta)
            if method in {"POST", "PUT", "PATCH"}:
                HttpxArgsHandler._add_body_args(meta, args)
            else:
                HttpxArgsHandler._add_content_arg(meta, args)

            return {k: v for k, v in args.items() if v is not None}
        except InvalidHttpMethodError as e:
            raise InvalidHttpxArgumentsError(f"Invalid arguments for httpx: {e}")
        except Exception as e:
            raise InvalidHttpxArgumentsError(f"Invalid arguments for httpx: {e}")

    @staticmethod
    def _build_common_args(meta: Any) -> Dict[str, Any]:
        """Build common arguments for httpx requests from the Meta object.

        Args:
            meta (Any): The Meta object containing request metadata.

        Returns:
            Dict[str, Any]: The common arguments for httpx requests.
        """

        def empty_to_none(value: Any) -> Any:
            if isinstance(value, Box) and not value:
                return None
            return value

        return {
            "params": empty_to_none(
                meta._attributes.params.to_dict() if meta._attributes.params else None
            ),
            "headers": empty_to_none(
                meta._attributes.headers.to_dict() if meta._attributes.headers else None
            ),
            "cookies": empty_to_none(
                meta._attributes.cookies.to_dict() if meta._attributes.cookies else None
            ),
            "auth": meta._attributes.auth,
            "follow_redirects": meta._attributes.follow_redirects,
            "timeout": meta._attributes.timeout,
            "extensions": empty_to_none(
                meta._attributes.extensions.to_dict()
                if meta._attributes.extensions
                else None
            ),
        }

    @staticmethod
    def _add_body_args(meta: Any, args: Dict[str, Any]) -> None:
        """Add body arguments for httpx requests from the Meta object.

        Args:
            meta (Any): The Meta object containing request metadata.
            args (Dict[str, Any]): The arguments dictionary to update.
        """

        def box_to_dict_or_value(value: Any) -> Any:
            if isinstance(value, Box):
                return value.to_dict()
            return value

        if meta._attributes.json:
            args["json"] = box_to_dict_or_value(meta._attributes.json)
        elif meta._attributes.data:
            args["data"] = box_to_dict_or_value(meta._attributes.data)
        elif meta._attributes.files:
            args["files"] = box_to_dict_or_value(meta._attributes.files)
        elif meta._attributes.content:
            args["content"] = HttpxArgsHandler._box_to_string_or_bytes(
                meta._attributes.content
            )

    @staticmethod
    def _add_content_arg(meta: Any, args: Dict[str, Any]) -> None:
        """Add content argument for httpx requests from the Meta object.

        Args:
            meta (Any): The Meta object containing request metadata.
            args (Dict[str, Any]): The arguments dictionary to update.
        """
        if meta._attributes.content:
            args["content"] = HttpxArgsHandler._box_to_string_or_bytes(
                meta._attributes.content
            )

    @staticmethod
    def _box_to_string_or_bytes(value: Any) -> Any:
        """Convert a Box object to a string or bytes.

        Args:
            value (Any): The Box object to convert.

        Returns:
            Any: The string or bytes representation of the Box object.
        """
        if isinstance(value, Box):
            return value.to_json()
        return value
