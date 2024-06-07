
from beaver_routes.core.meta import Meta
from beaver_routes.core.hook import Hook
import httpx


async def route_request_hook(method: str, url: str, meta: Meta) -> None:
    print(f"Route request hook: {method} {url} {meta}")
    meta.params.route_hook = "route_hook_value"


async def method_request_hook(method: str, url: str, meta: Meta) -> None:
    print(f"Method request hook: {method} {url} {meta}")
    meta.params.method_hook = "method_hook_value"


async def scenario_request_hook(method: str, url: str, meta: Meta) -> None:
    print(f"Scenario request hook: {method} {url} {meta}")
    meta.params.scenario_hook = "scenario_hook_value"


async def route_response_hook(response: httpx.Response) -> None:
    print(f"Route response hook: {response.status_code}")


async def method_response_hook(response: httpx.Response) -> None:
    print(f"Method response hook: {response.status_code}")


async def scenario_response_hook(response: httpx.Response) -> None:
    print(f"Scenario response hook: {response.status_code}")

