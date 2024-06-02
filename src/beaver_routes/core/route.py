from __future__ import annotations

import inspect
import logging
from typing import Any, Callable

import requests

from beaver_routes.core.attribute_dictionary import AttributeDictionary
from beaver_routes.core.base_mixin import BaseMixin
from beaver_routes.core.config import Config
from beaver_routes.core.constants import (
    ALLOWED_COMMON_PARAMS,
    ALLOWED_METHOD_PARAMS,
    VALID_HOOK_SCENARIOS,
    VALID_MERGE_STRATEGIES,
)

logger = logging.getLogger(__name__)


class BaseRoute(BaseMixin):
    """
    Base class for defining API request routes

    Attribute:
        BASE_URL (str): The base URL for the API. class level variable to set API's root URL
        scenario_method (dict[str, Any]): Scenario method when a route is called for specific scenario
        endpoint (str|None): The endpoint URI for the route. should be defined in derived route

    Raises:
        TypeError:
            When given after hook is not callable
            When route method has more than one parameter
        NotImplementedError:
            When request method attribute is not defined for the route
            When validator or named validator is not defined in the derived route
        KeyError: When invalid attribute is present in the request attributes
        AttributeError: When scenario method is not found in for_scenario call
        ValueError: When invalid request arguments merge strategy is provided

    Examples:
    ```python

    # create Route
    class PongRoute:
        def __init__(self) -> None:
            super().__init__(endpoint="/pong")

        def __route__(self):
            request_attributes = {
                "endpoint": "/pong",
                "params": {"username": "John Doe", "id": 3149232},
            }

            return request_attributes

        def __get__(self):
            return {
                "params": {"firstname": "John", "lastname": "Doe"},
            }

        def pong(self):
            return {"params": {"username": "Jane Doe"}}


    pong_route = PongRoute()

    # make request with existing params in __route__() and method
    response = pong_route.get()

    # making request for a scenario
    response = pong_route.for_scenario("pong").get(**{"params": {"firstname": "Jane", "DOB": "00000000"}})

    # passing additional parameters to the request
    response = pong_route.get(**{"params": {"firstname": "Jane", "DOB": "00000000"}})
    ```
    """

    BASE_URL: str = Config.BASE_URL  # Base API URL, should be read from config
    CONFIG: dict[Any, Any] = Config.CONFIG

    def __init__(self, endpoint: str = "") -> None:
        super().__init__(endpoint)

    def __route__(self) -> dict[str, Any]:
        """
        This method returns the attributes that are common throughout the methods supported by route.

        The request attributes will be defined in individual routes that inherit the Route
        """
        return {}

    def for_scenario(self, scenario_name: str, group_name: str = None) -> BaseRoute:
        """
        Set Scenario specific attributes for the route and return the updated instance

        Args:
            scenario_name (str): the name of scenario to set attributes for

        Returns:
            BaseRoute: The instance with updated scenario attribute
        """

        if group_name:
            scenario_group_instance = self._get_scenario_group(group_name)
        else:
            scenario_group_instance = self

        self.current_scenario_group = group_name
        self.current_scenario_name = scenario_name
        scenario_method = getattr(scenario_group_instance, scenario_name, None)
        group_class_name = scenario_group_instance.__class__.__name__

        if scenario_name and callable(scenario_method):
            logger.info(
                f"setting scenario attributes to route from scenario: '{scenario_name}', group: '{group_class_name}'"
            )
            self.scenario_method = scenario_method
        else:
            error_message = f"Cannot find scenario method for '{scenario_name}' in '{group_class_name}'"
            logger.error(error_message)
            raise AttributeError(error_message)
        return self

    def _get_scenario_group(self, group_name: str):
        """
        Fetched scenario group instance from derived route

        Args:
            group_name (str): group name defined in derived route

        Raises:
            AttributeError: when scenario groups attribute not defined in derived route
            KeyError: when group is not defined in derived route
            TypeError: when scenario group type is a class type

        Returns:
            object: scenario group instance
        """

        if not self.scenario_groups:
            error_message = "'scenario_groups' not define in derived route"
            logger.error(error_message)
            raise AttributeError(error_message)

        scenario_group = self.scenario_groups.get(group_name)
        if not scenario_group:
            error_message = f"scenario group name: {group_name} not defined in derived route 'scenario_groups'"
            logger.error(error_message)
            raise KeyError(error_message)

        if not isinstance(scenario_group, type):
            error_message = f"scenario group is should be a 'class type', not {type(scenario_group)}"
            logger.error(error_message)
            raise TypeError(error_message)

        scenario_group_instance = scenario_group()
        scenario_group_instance.route = self

        return scenario_group_instance

    def _get_request_args(
        self, method: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Returns the processed request args

        Get the merged request arguments including route, method, scenario arguments and **kwargs,
        and remove the ignored args from the merged request arguments

        Args:
            method (str): The HTTP request method
            kwargs (dict[str, Any]): request arguments

        Returns:
            dict[str, Any]: The merged and processed request arguments
        """

        # clear after hooks map
        self._after_hooks = {}

        route_attribute = self._invoke_with_arg_dict_conditionally(self.__route__)
        method = self._get_request_method(method)
        method_attribute = (
            self._invoke_with_arg_dict_conditionally(method) if method else {}
        )
        scenario_attribute = (
            self._invoke_with_arg_dict_conditionally(self.scenario_method)
            if self.scenario_method
            else {}
        )

        request_args = self._merge_request_args(
            route_attribute, method_attribute, scenario_attribute, kwargs
        )

        return request_args

    def _invoke_with_arg_dict_conditionally(
        self, route_method: Callable
    ) -> AttributeDictionary | dict:
        """
        Execute the given route method conditionally based on number of parameters it accepts
        passes argument dictionary instance as parameter if method accept one parameter

        Args:
            route_method (Callable): route method

        Raises:
            TypeError: when route method has more than one parameter

        Returns:
            AttributeDictionary | dict: result of calling route method or attribute dictionary
        """
        method_parameters = inspect.signature(route_method).parameters.keys()
        if len(method_parameters) > 1:
            error_message = f"method execution failed, '{route_method}' route method does not support more than 1 request argument"
            logger.error(error_message)
            raise TypeError(error_message)

        if len(method_parameters) == 1:
            scenario_attributes = AttributeDictionary()
            route_method(scenario_attributes)
        else:
            scenario_attributes = route_method()

        return scenario_attributes

    def _merge_request_args(self, *request_args: dict[str, Any]) -> dict[str, Any]:
        """
        Merge dictionaries of request arguments

        Args:
            request_args (dict[str, Any]): route, method, scenario arguments and provided kwargs to merge

        Returns:
            dict[str, Any]: The merged request arguments
        """
        merged_args = {}

        for dictionary in request_args:
            if isinstance(dictionary, AttributeDictionary):
                dictionary = dictionary.to_dict()
            for key, value in dictionary.items():
                if isinstance(value, AttributeDictionary):
                    value = value.to_dict()
                if (
                    key in merged_args
                    and isinstance(merged_args[key], dict)
                    and isinstance(value, dict)
                ):
                    merge_strategy = value.pop("_merge_strategy", "deep_merge")

                    if merge_strategy == "deep_merge":
                        merged_args[key] = self._merge_request_args(
                            merged_args[key], value
                        )
                    elif merge_strategy == "replace":
                        merged_args[key] = value
                    elif merge_strategy == "remove":
                        merged_args.pop(key)
                    else:
                        raise ValueError(
                            f"invalid merge strategy: '{merge_strategy}'. "
                            f"valid merge strategies: {*VALID_MERGE_STRATEGIES,}"
                        )

                else:
                    if key == "_merge_strategy":
                        continue
                    if isinstance(value, dict):
                        value.pop("_merge_strategy", None)

                    merged_args[key] = value

        return merged_args

    def set_after_hooks(self, scope: str, hooks: list[Callable]):
        """
        Set hooks to execute after sending a request.

        The priority of hooks execution by scope is route, method, scenario

        Args:
            scope (str): Scope for the after hooks. Ex: `route`, `method`, `scenario`.
            hooks (list[Callable]): List of hooks for the given scope

        Raises:
            KeyError: When invalid scope is provided
            TypeError: When hook is not callable
        """
        if scope not in VALID_HOOK_SCENARIOS:
            error = f"scope: '{scope}' is not a valid hook scope. valid scopes: {*VALID_HOOK_SCENARIOS,}"
            logger.error(error)
            raise KeyError(error)

        for hook in hooks:
            if not callable(hook):
                error_message = (
                    f"Invalid after hook: '{hook}', 'after hook' should be a callable"
                )
                logger.error(error_message)
                raise TypeError(error_message)

        logger.debug(
            f"setting hooks: {hooks} for scope: {scope} for route: '{self.__class__.__name__}'"
        )
        self._after_hooks[scope] = hooks

    def _execute_after_hooks(self):
        """
        Execute after hooks for the route
        """
        route_hooks = self._after_hooks.get("route", [])
        method_hooks = self._after_hooks.get("method", [])
        scenario_hooks = self._after_hooks.get("scenario", [])

        hooks = route_hooks + method_hooks + scenario_hooks
        logger.debug(f"executing after hooks {hooks}")
        for hook in hooks:
            hook()

    def _get_request_method(self, method: str) -> Callable | None:
        """
        Get request method of route by calling __<method>__,
        None if the method is not defined in route

        Args:
            method (str): The Http request method

        Returns:
            Callable | None: request method of route
        """

        logger.debug(f"Getting request method: {method} from route")
        route_method = getattr(self, f"__{method}__", None)
        if route_method:
            return route_method
        else:
            logger.debug(f"method attribute for '{method}' not implemented in route")

    def get_parsed_request_args(
        self, method: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """
        merges and validate the request args and returns parsed request args

        Args:
            method (str): The Http request method

        Raises:
            AttributeError: when api endpoint is not defined in route
            KeyError: When Invalid attribute is found in request attributes

        Returns:
            dict[str, Any]: merged and parsed request args
        """
        request_args = self._get_request_args(method, **kwargs)

        url_placeholders = request_args.pop("url_placeholders", {})

        # create request url if not in request parameters
        if "url" not in request_args:
            if not self.endpoint:
                error_message = (
                    "request args does not contain 'endpoint' to send request"
                )
                logger.error(error_message)
                raise AttributeError(error_message)
            request_url = self.BASE_URL + self.endpoint
            request_args["url"] = request_url.format(**url_placeholders)

        # validate request parameters
        allowed_request_params = (
            ALLOWED_COMMON_PARAMS + ALLOWED_METHOD_PARAMS[method.upper()]
        )
        request_args_keys = request_args.keys()
        if set(request_args_keys).issubset(allowed_request_params):
            logger.debug("request args are valid")
        else:
            invalid_args = set(request_args_keys) - set(allowed_request_params)
            error_message = f"request args contains invalid kwargs, invalid keys: {invalid_args}, method: '{method}'"
            logger.error(error_message)
            raise KeyError(error_message)

        return request_args

    def _request(
        self, method: str, **kwargs: dict[str, Any]
    ) -> requests.Response | None:
        """
        Send the HTTP request after validating the request attributes

        Args:
            method (str): The Http request method
            kwargs (dict[str, Any]): Additional request arguments

        Raises:
            KeyError: When invalid attribute is found in request attributes

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """

        self._request_args = self.get_parsed_request_args(method, **kwargs)
        response = requests.request(method=method, **self._request_args)
        self._response = response

        # execute after hooks with priority
        self._execute_after_hooks()

        return response

    @property
    def request_args(self) -> dict[str, Any]:
        return self._request_args

    @property
    def response(self) -> requests.Response | None:
        return self._response

    def validator(self, *args, **kwargs):
        raise NotImplementedError("validator should defined in derived route")

    def validate(self, *args, **kwargs):
        validator_name = kwargs.pop("name", "validator")
        validator = getattr(self, validator_name, None)

        if validator and callable(validator):
            validator(*args, **kwargs)
        else:
            raise NotImplementedError(
                f"Validation attribute '{validator_name}' not found in derived route"
            )

    def get(self, **kwargs: dict[str, Any]) -> requests.Response | None:
        """
        Send a GET request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("get", **kwargs)

    def options(self, **kwargs) -> requests.Response | None:
        """
        Send a OPTIONS request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("options", **kwargs)

    def head(self, **kwargs) -> requests.Response | None:
        """
        Send a HEAD request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("head", **kwargs)

    def post(self, **kwargs) -> requests.Response | None:
        """
        Send a POST request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("post", **kwargs)

    def put(self, **kwargs) -> requests.Response | None:
        """
        Send a PUT request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("put", **kwargs)

    def patch(self, **kwargs) -> requests.Response | None:
        """
        Send a PATCH request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("patch", **kwargs)

    def delete(self, **kwargs) -> requests.Response | None:
        """
        Send a DELETE request

        Args:
            kwargs (dict[str, Any]): Additional request arguments

        Returns:
            requests.Response | None: The response from the http request, or None on failure.
        """
        return self._request("delete", **kwargs)

    def __str__(self) -> str:
        return (
            f"BASE_URL: '{self.BASE_URL}', scenario_group: '{self.current_scenario_group}', "
            f"scenario_method: '{self.current_scenario_name}', endpoint: '{self.endpoint}'"
        )

    def __repr__(self) -> str:
        return (
            f"BaseRoute(BASE_URL: '{self.BASE_URL}', scenario_group: '{self.current_scenario_group}', "
            f"scenario_method: '{self.current_scenario_name}', endpoint: '{self.endpoint}')"
        )


class Route(BaseRoute):
    pass
