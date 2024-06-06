from typing import Any, Dict
from box import Box
from beaver_routes.exceptions.exceptions import InvalidHttpMethodError, InvalidHttpxArgumentsError

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

        try:
            args = {
                "method": method,
                "url": meta.url,
                "params": empty_to_none(meta._attributes.params.to_dict() if meta._attributes.params else None),
                "headers": empty_to_none(meta._attributes.headers.to_dict() if meta._attributes.headers else None),
                "cookies": empty_to_none(meta._attributes.cookies.to_dict() if meta._attributes.cookies else None),
                "auth": meta._attributes.auth,
                "follow_redirects": meta._attributes.follow_redirects,
                "timeout": meta._attributes.timeout,
                "extensions": empty_to_none(meta._attributes.extensions.to_dict() if meta._attributes.extensions else None),
            }

            if method in {"POST", "PUT", "PATCH"}:
                args.update({
                    "content": meta._attributes.content,
                    "data": empty_to_none(meta._attributes.data.to_dict() if isinstance(meta._attributes.data, Box) else meta._attributes.data),
                    "files": empty_to_none(meta._attributes.files.to_dict() if isinstance(meta._attributes.files, Box) else meta._attributes.files),
                    "json": empty_to_none(meta._attributes.json.to_dict() if isinstance(meta._attributes.json, Box) else meta._attributes.json),
                })

            # Remove keys with None values
            return {k: v for k, v in args.items() if v is not None}
        except InvalidHttpMethodError as e:
            raise InvalidHttpxArgumentsError(f"Invalid arguments for httpx: {e}")
        except Exception as e:
            raise InvalidHttpxArgumentsError(f"Invalid arguments for httpx: {e}")
