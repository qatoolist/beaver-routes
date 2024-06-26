from beaver_routes.core.base_route import BaseRoute
from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta
from beaver_routes.core.response import Response


class CustomRoute(BaseRoute):
    """Custom route class for testing and demonstration purposes.

    This class demonstrates how to customize a route by overriding the hook and HTTP method
    handlers. It provides examples of adding hooks and setting metadata for various HTTP methods.

    Methods:
        __route__(meta: Meta, hooks: Hook) -> None:
            Customize the route-specific metadata and hooks.
        __get__(meta: Meta, hooks: Hook) -> None:
            Customize the GET-specific metadata and hooks.
        __post__(meta: Meta, hooks: Hook) -> None:
            Customize the POST-specific metadata and hooks.
        __put__(meta: Meta, hooks: Hook) -> None:
            Customize the PUT-specific metadata and hooks.
        __delete__(meta: Meta, hooks: Hook) -> None:
            Customize the DELETE-specific metadata and hooks.
        scenario1(meta: Meta, hooks: Hook) -> None:
            Define a scenario to customize metadata and hooks for testing.
    """

    def __route__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the route-specific metadata and hooks.

        Args:
            meta (Meta): The route metadata.
            hooks (Hook): The route hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__route__(Meta(), Hook())
        """
        hooks.add("request", self.route_request_hook)
        hooks.add("response", self.route_response_hook)
        meta.params.route_param = "route_value"

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the GET-specific metadata and hooks.

        Args:
            meta (Meta): The GET request metadata.
            hooks (Hook): The GET request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__get__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.get_param = "get_value"

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the POST-specific metadata and hooks.

        Args:
            meta (Meta): The POST request metadata.
            hooks (Hook): The POST request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__post__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.post_param = "post_value"

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the PUT-specific metadata and hooks.

        Args:
            meta (Meta): The PUT request metadata.
            hooks (Hook): The PUT request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__put__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.put_param = "put_value"

    def __delete__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the DELETE-specific metadata and hooks.

        Args:
            meta (Meta): The DELETE request metadata.
            hooks (Hook): The DELETE request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__delete__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.delete_param = "delete_value"

    def __patch__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the PATCH-specific metadata and hooks.

        Args:
            meta (Meta): The PATCH request metadata.
            hooks (Hook): The PATCH request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__patch__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.patch_param = "patch_value"

    def __head__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the HEAD-specific metadata and hooks.

        Args:
            meta (Meta): The HEAD request metadata.
            hooks (Hook): The HEAD request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__head__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.head_param = "head_value"

    def __options__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the OPTIONS-specific metadata and hooks.

        Args:
            meta (Meta): The OPTIONS request metadata.
            hooks (Hook): The OPTIONS request hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.__options__(Meta(), Hook())
        """
        hooks.add("request", self.method_request_hook)
        hooks.add("response", self.method_response_hook)
        meta.params.options_param = "options_value"

    def scenario1(self, meta: Meta, hooks: Hook) -> None:
        """Define a scenario to customize metadata and hooks for testing.

        Args:
            meta (Meta): The scenario metadata.
            hooks (Hook): The scenario hooks.

        Example:
            >>> route = CustomRoute()
            >>> route.scenario1(Meta(), Hook())
        """
        hooks.add("request", self.scenario_request_hook)
        hooks.add("response", self.scenario_response_hook)
        meta.params.scenario_param = "scenario_value"

    def route_request_hook(self, method: str, url: str, meta: Meta) -> None:
        """Example route request hook.

        Args:
            method (str): The HTTP method.
            url (str): The request URL.
            meta (Meta): The request metadata.

        Example:
            >>> route_request_hook("GET", "http://example.com", Meta())
        """
        print(f"Route request hook: {method} {url} {meta}")
        meta.params.route_hook = "route_hook_value"

    def method_request_hook(self, method: str, url: str, meta: Meta) -> None:
        """Example method request hook.

        Args:
            method (str): The HTTP method.
            url (str): The request URL.
            meta (Meta): The request metadata.

        Example:
            >>> method_request_hook("GET", "http://example.com", Meta())
        """
        print(f"Method request hook: {method} {url} {meta}")
        meta.params.method_hook = "method_hook_value"

    def scenario_request_hook(self, method: str, url: str, meta: Meta) -> None:
        """Example scenario request hook.

        Args:
            method (str): The HTTP method.
            url (str): The request URL.
            meta (Meta): The request metadata.

        Example:
            >>> scenario_request_hook("GET", "http://example.com", Meta())
        """
        print(f"Scenario request hook: {method} {url} {meta}")
        meta.params.scenario_hook = "scenario_hook_value"

    def route_response_hook(self, response: Response) -> None:
        """Example route response hook.

        Args:
            response (Response): The HTTP response.

        Example:
            >>> route_response_hook(Response(status_code=HTTPStatus.OK))
        """
        print(f"Route response hook: {response.status_code}")

    def method_response_hook(self, response: Response) -> None:
        """Example method response hook.

        Args:
            response (Response): The HTTP response.

        Example:
            >>> method_response_hook(Response(status_code=HTTPStatus.OK))
        """
        print(f"Method response hook: {response.status_code}")

    def scenario_response_hook(self, response: Response) -> None:
        """Example scenario response hook.

        Args:
            response (Response): The HTTP response.

        Example:
            >>> scenario_response_hook(Response(status_code=HTTPStatus.OK))
        """
        print(f"Scenario response hook: {response.status_code}")
