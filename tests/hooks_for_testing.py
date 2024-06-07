import httpx

from beaver_routes.core.meta import Meta


async def route_request_hook(method: str, url: str, meta: Meta) -> None:
    """Example route request hook.

    Args:
        method (str): The HTTP method.
        url (str): The request URL.
        meta (Meta): The request metadata.

    Example:
        >>> await route_request_hook("GET", "http://example.com", Meta())
    """
    print(f"Route request hook: {method} {url} {meta}")
    meta.params.route_hook = "route_hook_value"


async def method_request_hook(method: str, url: str, meta: Meta) -> None:
    """Example method request hook.

    Args:
        method (str): The HTTP method.
        url (str): The request URL.
        meta (Meta): The request metadata.

    Example:
        >>> await method_request_hook("GET", "http://example.com", Meta())
    """
    print(f"Method request hook: {method} {url} {meta}")
    meta.params.method_hook = "method_hook_value"


async def scenario_request_hook(method: str, url: str, meta: Meta) -> None:
    """Example scenario request hook.

    Args:
        method (str): The HTTP method.
        url (str): The request URL.
        meta (Meta): The request metadata.

    Example:
        >>> await scenario_request_hook("GET", "http://example.com", Meta())
    """
    print(f"Scenario request hook: {method} {url} {meta}")
    meta.params.scenario_hook = "scenario_hook_value"


async def route_response_hook(response: httpx.Response) -> None:
    """Example route response hook.

    Args:
        response (httpx.Response): The HTTP response.

    Example:
        >>> await route_response_hook(httpx.Response(status_code=HTTPStatus.OK))
    """
    print(f"Route response hook: {response.status_code}")


async def method_response_hook(response: httpx.Response) -> None:
    """Example method response hook.

    Args:
        response (httpx.Response): The HTTP response.

    Example:
        >>> await method_response_hook(httpx.Response(status_code=HTTPStatus.OK))
    """
    print(f"Method response hook: {response.status_code}")


async def scenario_response_hook(response: httpx.Response) -> None:
    """Example scenario response hook.

    Args:
        response (httpx.Response): The HTTP response.

    Example:
        >>> await scenario_response_hook(httpx.Response(status_code=HTTPStatus.OK))
    """
    print(f"Scenario response hook: {response.status_code}")
