from __future__ import annotations

import inspect
import logging
from typing import Any, Callable, Optional

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
    BASE_URL: str = Config.BASE_URL  # Use configuration
    CONFIG: dict[Any, Any] = Config.CONFIG

    def __init__(self, endpoint: str = "") -> None:
        super().__init__(endpoint)

    def __route__(self) -> dict[str, Any]:
        return {}

    def for_scenario(
        self, scenario_name: str, group_name: Optional[str] = None
    ) -> BaseRoute:
        if group_name:
            scenario_group_instance = self._get_scenario_group(group_name)
        else:
            scenario_group_instance = self

        self.current_scenario_group = group_name
        self.current_scenario_name = scenario_name
        scenario_method: Optional[Callable[..., Any]] = getattr(
            scenario_group_instance, scenario_name, None
        )
        group_class_name = scenario_group_instance.__class__.__name__

        if scenario_method and callable(scenario_method):
            logger.info(
                f"setting scenario attributes to route from scenario: '{scenario_name}', group: '{group_class_name}'"
            )
            self.scenario_method = scenario_method
        else:
            error_message = f"Cannot find scenario method for '{scenario_name}' in '{group_class_name}'"
            logger.error(error_message)
            raise AttributeError(error_message)
        return self

    def _get_scenario_group(self, group_name: str) -> Any:
        if not self.scenario_groups:
            error_message = "'scenario_groups' not defined in derived route"
            logger.error(error_message)
            raise AttributeError(error_message)

        scenario_group = self.scenario_groups.get(group_name)
        if not scenario_group:
            error_message = f"scenario group name: {group_name} not defined in derived route 'scenario_groups'"
            logger.error(error_message)
            raise KeyError(error_message)

        if not isinstance(scenario_group, type):
            error_message = (
                f"scenario group should be a 'class type', not {type(scenario_group)}"
            )
            logger.error(error_message)
            raise TypeError(error_message)

        scenario_group_instance = scenario_group()
        scenario_group_instance.route = self

        return scenario_group_instance

    def _get_request_args(
        self, method: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        self._after_hooks = {}

        route_attribute = self._invoke_with_arg_dict_conditionally(self.__route__)
        request_method = self._get_request_method(method)
        method_attribute = (
            self._invoke_with_arg_dict_conditionally(request_method)
            if request_method
            else {}
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
        self, route_method: Optional[Callable[..., Any]]
    ) -> dict[str, Any]:
        if not route_method:
            return {}

        method_parameters = inspect.signature(route_method).parameters.keys()
        if len(method_parameters) > 1:
            error_message = f"method execution failed, '{route_method}' route method does not support more than 1 request argument"
            logger.error(error_message)
            raise TypeError(error_message)

        scenario_attributes: AttributeDictionary | dict[Any, Any] = {}

        if len(method_parameters) == 1:
            scenario_attributes = AttributeDictionary()
            route_method(scenario_attributes)
        else:
            scenario_attributes = route_method()

        if isinstance(scenario_attributes, AttributeDictionary):
            scenario_attributes = scenario_attributes.to_dict()

        return scenario_attributes

    def _merge_request_args(self, *request_args: dict[str, Any]) -> dict[str, Any]:
        merged_args: dict[str, Any] = {}

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

    def set_after_hooks(self, scope: str, hooks: list[Callable[..., Any]]) -> None:
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

    def _execute_after_hooks(self) -> None:
        route_hooks = self._after_hooks.get("route", [])
        method_hooks = self._after_hooks.get("method", [])
        scenario_hooks = self._after_hooks.get("scenario", [])

        hooks = route_hooks + method_hooks + scenario_hooks
        logger.debug(f"executing after hooks {hooks}")
        for hook in hooks:
            hook()

    def _get_request_method(self, method: str) -> Optional[Callable[..., Any]]:
        logger.debug(f"Getting request method: {method} from route")
        route_method: Optional[Callable[..., Any]] = getattr(
            self, f"__{method}__", None
        )
        if route_method:
            return route_method
        else:
            logger.debug(f"method attribute for '{method}' not implemented in route")

            return None

    def get_parsed_request_args(
        self, method: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        request_args = self._get_request_args(method, **kwargs)

        url_placeholders = request_args.pop("url_placeholders", {})

        if "url" not in request_args:
            if not self.endpoint:
                error_message = "request args do not contain 'endpoint' to send request"
                logger.error(error_message)
                raise AttributeError(error_message)
            request_url = self.BASE_URL + self.endpoint
            request_args["url"] = request_url.format(**url_placeholders)

        allowed_request_params = (
            ALLOWED_COMMON_PARAMS + ALLOWED_METHOD_PARAMS[method.upper()]
        )
        request_args_keys = request_args.keys()
        if set(request_args_keys).issubset(allowed_request_params):
            logger.debug("request args are valid")
        else:
            invalid_args = set(request_args_keys) - set(allowed_request_params)
            error_message = f"request args contain invalid kwargs, invalid keys: {invalid_args}, method: '{method}'"
            logger.error(error_message)
            raise KeyError(error_message)

        return request_args

    def _request(
        self, method: str, **kwargs: dict[str, Any]
    ) -> Optional[requests.Response]:
        self._request_args = self.get_parsed_request_args(method, **kwargs)
        response = requests.request(method=method, **self._request_args)
        self._response = response

        self._execute_after_hooks()

        return response

    @property
    def request_args(self) -> dict[str, Any] | None:
        return self._request_args

    @property
    def response(self) -> Optional[requests.Response]:
        return self._response

    def validator(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError("validator should be defined in derived route")

    def validate(self, *args: Any, **kwargs: Any) -> None:
        validator_name = kwargs.pop("name", "validator")
        validator = getattr(self, validator_name, None)

        if validator and callable(validator):
            validator(*args, **kwargs)
        else:
            raise NotImplementedError(
                f"Validation attribute '{validator_name}' not found in derived route"
            )

    def get(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
        return self._request("get", **kwargs)

    def options(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
        return self._request("options", **kwargs)

    def head(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
        return self._request("head", **kwargs)

    def post(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
        return self._request("post", **kwargs)

    def put(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
        return self._request("put", **kwargs)

    def patch(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
        return self._request("patch", **kwargs)

    def delete(self, **kwargs: dict[str, Any]) -> Optional[requests.Response]:
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
