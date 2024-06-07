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
        def box_to_dict_or_value(value: Any) -> Any:
            if isinstance(value, Box):
                return value.to_dict()
            return value

        if meta._attributes.json is not None:
            args["json"] = box_to_dict_or_value(meta._attributes.json)
        elif meta._attributes.data is not None:
            args["data"] = box_to_dict_or_value(meta._attributes.data)
        elif meta._attributes.files is not None:
            args["files"] = box_to_dict_or_value(meta._attributes.files)
        elif meta._attributes.content is not None:
            args["content"] = HttpxArgsHandler._box_to_string_or_bytes(
                meta._attributes.content
            )

    @staticmethod
    def _add_content_arg(meta: Any, args: Dict[str, Any]) -> None:
        if meta._attributes.content is not None:
            args["content"] = HttpxArgsHandler._box_to_string_or_bytes(
                meta._attributes.content
            )

    @staticmethod
    def _box_to_string_or_bytes(value: Any) -> Any:
        if isinstance(value, Box):
            return value.to_json()
        return value
