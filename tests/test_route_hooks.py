from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from tests.mock.mock_requests import mock_request_side_effect
from tests.mock_routes import VerifyRoute

class TestRouteHooks:
    @pytest.fixture
    def verify_route(self):
        return VerifyRoute()

    def setup_method(self):
        self.mock_hook = Mock()

    @pytest.mark.skip(reason="TEAMNADO-6788")
    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_hook_trigger(self, mock_request, verify_route):
        scenario_mock_hook = [Mock()]
        method_mock_hooks = [Mock()]
        route_mock_hooks = [Mock()]
        verify_route.scenario_mock_hooks = scenario_mock_hook
        verify_route.method_mock_hooks = method_mock_hooks
        verify_route.route_mock_hooks = route_mock_hooks
        valid_key_route = verify_route.for_scenario("valid_user")

        mock_after_hooks = scenario_mock_hook + method_mock_hooks + route_mock_hooks

        valid_key_route.get()

        # validate all hooks are called only once
        for mock_function in mock_after_hooks:
            mock_function.assert_called_once()

        # validate hooks are called in specified order
        excepted_calls = [
            mock.call.route,
            mock.call.method,
            mock.call.scenario,
        ]
        self.mock_hook.assert_has_calls(excepted_calls)
