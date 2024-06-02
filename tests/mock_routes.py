from beaver_routes.core.route import Route
from tests.mock_scenarios import PongScenarios


class VerifyRoute(Route):
    """
    Sample Route showing how routes will be created
    """

    def __init__(self) -> None:
        super().__init__(endpoint="/verify")
        self.scenario_mock_hooks = None
        self.method_mock_hooks = None
        self.route_mock_hooks = None

    def __route__(self):
        if self.route_mock_hooks:
            self.set_after_hooks("route", self.route_mock_hooks)
        request_attributes = {
            "timeout": 10,
            "allow_redirects": False,
            "verify": False,
            "stream": False,
            "cert": "",
        }

        return request_attributes

    def __get__(self):
        if self.method_mock_hooks:
            self.set_after_hooks("method", self.method_mock_hooks)
        return {
            "params": {},
            "headers": {},
            "cookies": {},
            "auth": {},
            "allow_redirects": False,
            "proxies": {},
            "verify": False,
            "stream": False,
            "cert": "",
        }

    def invalid_key(self):
        return {"params": {"key": "invalid"}}

    def valid_key(self):
        return {"params": {"key": 3149232}}

    def valid_user(self):
        if self.scenario_mock_hooks:
            self.set_after_hooks("scenario", self.scenario_mock_hooks)
        return {
            "timeout": 30,
        }


class PongRoute(Route):
    """
    Sample Route for testing merging of args in route
    """

    def __init__(self) -> None:
        super().__init__(endpoint="/pong")
        self.route_attributes = None
        self.method_attributes = None
        self.scenario_attributes = None

    def __route__(self):
        request_attributes = {
            "params": {"username": "John Doe", "id": 3149232},
        }

        return self.route_attributes or request_attributes

    def __get__(self):
        request_attributes = {
            "params": {"firstname": "John", "lastname": "Doe"},
        }
        return self.method_attributes or request_attributes

    def __post__(self):
        return self.method_attributes or {}

    def pong(self):
        request_attributes = {"params": {"username": "Jane Doe"}}
        return self.scenario_attributes or request_attributes

    def pong_validator(self):
        pass

    def scenario_with_attribute_dictionary(self, request_args):
        request_args.json.user = {"data3": "value3"}


class GroupPongRoute(Route):
    """
    Sample Route for testing merging of args in route
    """

    def __init__(self) -> None:
        super().__init__(endpoint="/pong")
        self.scenario_groups = {"pong_scenario": PongScenarios}

    def __route__(self, request_args):
        request_args.params = {"username": "John Doe", "id": 3149232}

    def __get__(self, request_args):
        request_args.params = {"firstname": "John", "lastname": "Doe"}

    def __post__(self):
        return {}

    def with_leap_year_dob(self, request_args):
        request_args.params.userDetails = {"DOB": "29/02/1996"}
