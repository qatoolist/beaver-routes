from typing import Any, Dict

from box import Box

from beaver_routes.exceptions.exceptions import (
    InvalidHttpMethodError,
    InvalidHttpxArgumentsError,
)


class HttpxArgsHandler:
    @staticmethod
    def convert(meta: Any, method: str) -> Dict[str, Any]:
        valid_methods = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
        if method not in valid_methods:
            raise InvalidHttpMethodError(f"Invalid HTTP method: {method}")

        def empty_to_none(value: Any) -> Any:
            if isinstance(value, Box) and not value:
                return None
            return value

        def box_to_dict_or_value(value: Any) -> Any:
            if isinstance(value, Box):
                return value.to_dict()
            return value

        try:
            args = {
                "params": empty_to_none(
                    meta._attributes.params.to_dict()
                    if meta._attributes.params
                    else None
                ),
                "headers": empty_to_none(
                    meta._attributes.headers.to_dict()
                    if meta._attributes.headers
                    else None
                ),
                "cookies": empty_to_none(
                    meta._attributes.cookies.to_dict()
                    if meta._attributes.cookies
                    else None
                ),
                "auth": meta._attributes.auth,
                "follow_redirects": meta._attributes.follow_redirects,
                "timeout": meta._attributes.timeout,
                "extensions": empty_to_none(
                    meta._attributes.extensions.to_dict()
                    if meta._attributes.extensions
                    else None
                ),
                "content": box_to_dict_or_value(meta._attributes.content),
            }

            if method in {"POST", "PUT", "PATCH"}:
                args.update(
                    {
                        "content": box_to_dict_or_value(meta._attributes.content),
                        "data": box_to_dict_or_value(meta._attributes.data),
                        "files": box_to_dict_or_value(meta._attributes.files),
                        "json": box_to_dict_or_value(meta._attributes.json),
                    }
                )

            # Remove keys with None values
            return {k: v for k, v in args.items() if v is not None}
        except InvalidHttpMethodError as e:
            raise InvalidHttpxArgumentsError(f"Invalid arguments for httpx: {e}")
        except Exception as e:
            raise InvalidHttpxArgumentsError(f"Invalid arguments for httpx: {e}")
