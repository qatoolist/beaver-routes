import pytest

from beaver_routes.core.scenario import BaseScenario
from tests.mock_routes import GroupPongRoute


class TestBaseScenario:
    @pytest.fixture
    def route(self):
        return GroupPongRoute()

    def test_route_getter(self, route):
        base_scenario = BaseScenario()
        base_scenario._route = route
        assert base_scenario.route == route, "scenario route does not match with getter"

    def test_route_setter(self, route):
        base_scenario = BaseScenario()
        base_scenario.route = route
        assert (
            base_scenario._route == route
        ), "scenario route does not match with setter"

    def test_route_setter_invalid(self):
        base_scenario = BaseScenario()
        with pytest.raises(ValueError):
            base_scenario.route = "GroupPongRoute"
