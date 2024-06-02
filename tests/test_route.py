from unittest.mock import Mock, patch

import pytest

from beaver_routes.core.route import Route
from tests.mock.mock_requests import mock_request_side_effect
from tests.mock_routes import GroupPongRoute, PongRoute, VerifyRoute


class TestRoute:
    @pytest.fixture
    def verify_route(self):
        return VerifyRoute()

    @pytest.fixture
    def pong_route(self):
        return PongRoute()

    @patch("requests.request")
    def test_route_request_url(self, mock_request, verify_route):
        def mock_request_side_effect(url, **kwargs):
            response = Mock()
            response.status_code = 200
            response.json.return_value = kwargs
            response.request_url = url
            return response

        mock_request.side_effect = mock_request_side_effect
        response = verify_route.get()

        assert response.status_code == 200
        assert response.request_url == f"{VerifyRoute.BASE_URL}/verify"

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_valid_get_for_scenario(self, mock_request, verify_route):
        response = verify_route.for_scenario("invalid_key").get()
        assert response.status_code == 400
        assert response.json() == {"message": "bad key"}

        response = verify_route.for_scenario("valid_key").get()
        assert response.status_code == 200
        assert response.json() == {"message": "valid key"}

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_invalid_get_for_scenario(self, mock_request, verify_route):
        with pytest.raises(AttributeError):
            verify_route.for_scenario("does_not_exists").get()

    def test_for_scenario_route(self, verify_route):
        # validate 'for_scenario' return same route
        scenario_name = "valid_key"
        invalid_key_route = verify_route.for_scenario(scenario_name)

        assert id(invalid_key_route) == id(
            verify_route
        ), "scenario route and calling route should be same"
        assert verify_route.scenario_method, "scenario method not set to calling route"
        assert (
            verify_route.current_scenario_name == scenario_name
        ), "current scenario name did not match"

    def test_for_scenario_with_group_route(self):
        route = GroupPongRoute()
        scenario_name = "group_scenario"
        scenario_group_name = "pong_scenario"
        scenario_route = route.for_scenario(
            scenario_name, group_name=scenario_group_name
        )

        assert id(scenario_route) == id(
            route
        ), "scenario route and calling route should be same"
        assert route.scenario_method, "scenario method not set to calling route"
        assert (
            route.current_scenario_name == scenario_name
        ), "current scenario name did not match"
        assert (
            route.current_scenario_group == scenario_group_name
        ), "current scenario group name did not match"

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_invalid_request_args(self, mock_request, verify_route):
        with pytest.raises(KeyError):
            verify_route.get(**{"invalid": {"key": "1"}})

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_invalid_request_method(self, mock_request, verify_route):
        with pytest.raises(AttributeError):
            verify_route.for_scenario("valid_key").list()

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_argument_key_merge(self, mock_request, verify_route):
        # verify key overwrites if exists
        response = verify_route.for_scenario("valid_key").get(
            **{"params": {"key": "invalid"}}
        )
        assert response.status_code == 400
        assert response.json() == {"message": "bad key"}

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_argument_dictionary_merge(self, mock_request, verify_route):
        # verify dictionary does not overwrite (e.g. params) when merging
        response = verify_route.for_scenario("valid_key").get(
            **{"params": {"additional_key": "invalid"}}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "valid key"}

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_missing_endpoint(self, mock_request, verify_route):
        verify_route.endpoint = ""

        with pytest.raises(AttributeError):
            verify_route.get()

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_missing_endpoint_with_url(self, mock_request, verify_route):
        verify_route.endpoint = ""

        response = verify_route.for_scenario("valid_key").get(
            **{"url": "https://api.test.com/verify"}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "valid key"}

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_argument_merge_priority(self, mock_request, verify_route):
        # verify merging priority for request args
        pong_route = PongRoute()
        response = pong_route.for_scenario("pong").get(
            **{"params": {"firstname": "Jane", "DOB": "00000000"}}
        )
        expected_params = {
            "username": "Jane Doe",
            "id": 3149232,
            "firstname": "Jane",
            "lastname": "Doe",
            "DOB": "00000000",
        }
        assert response.status_code == 200
        assert response.json()["params"] == expected_params

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_request_args_property(self, mock_request, verify_route):
        scenario_route = verify_route.for_scenario("valid_key")
        _ = scenario_route.get(**{"params": {"additional_key1": "valid"}})

        # method not stored in request args
        mock_request.call_args.kwargs.pop("method")

        assert verify_route.request_args == mock_request.call_args.kwargs
        assert scenario_route.request_args == mock_request.call_args.kwargs

        _ = scenario_route.get(**{"params": {"additional_key2": "valid"}})
        mock_request.call_args.kwargs.pop("method")
        assert scenario_route.request_args == mock_request.call_args.kwargs

    @patch.object(Route, "CONFIG")
    def test_config(self, mock_config, verify_route):
        scenario_route = verify_route.for_scenario("valid_key")
        mock_config.test_value = "test"

        assert verify_route.CONFIG == mock_config
        assert verify_route.CONFIG.test_value == "test"
        assert scenario_route.CONFIG == mock_config
        assert scenario_route.CONFIG.test_value == "test"

    @patch("requests.request", return_value=Mock())
    def test_response_property(self, mock_request, pong_route):
        response = pong_route.get()

        assert response == mock_request.return_value

    @patch.object(PongRoute, "validator")
    def test_default_validator(self, validator, pong_route):
        args = ("test_arg1", "test_arg2")
        kwargs = {
            "expected__status_code": 201,
            "test_kw1": "test_kv1",
            "test_kw2": "test_kv2",
        }
        pong_route.validate(*args, *kwargs)

        validator.assert_called_once_with(*args, *kwargs)

    @patch.object(PongRoute, "pong_validator", return_value=None)
    def test_custom_validator(self, validator, pong_route):
        args = ("test_arg1", "test_arg2")
        kwargs = {
            "expected__status_code": 404,
            "test_kw1": "test_kv1",
            "test_kw2": "test_kv2",
        }
        pong_route.validate(*args, name="pong_validator", *kwargs)
        validator.assert_called_once_with(*args, *kwargs)

    @pytest.mark.skip(reason="not important as of now")
    def test_no_validator(self, pong_route):
        with pytest.raises(
            NotImplementedError, match="validator should defined in derived route"
        ):
            pong_route.validate()

    @pytest.mark.skip(reason="not important as of now")
    def test_invalid_validator(self, pong_route):
        validator_name = "ping_validator"
        expected_error = (
            f"Validation attribute '{validator_name}' not found in derived route"
        )
        with pytest.raises(NotImplementedError, match=expected_error):
            pong_route.validate(name="ping_validator")

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_url_placeholders(self, mock_request, verify_route):
        verify_route.endpoint = "/users/{id}"
        user_id = "user123"

        _ = verify_route.get(url_placeholders={"id": user_id})

        assert (
            mock_request.call_args.kwargs["url"]
            == f"{VerifyRoute.BASE_URL}/users/user123"
        )

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_merge_replace(self, mock_request, pong_route):
        pong_route.route_attributes = {
            "json": {"data1": "value1", "nested_key1": {"data1": "value1"}}
        }
        pong_route.method_attributes = {
            "json": {
                "data2": "value2",
                "nested_key1": {"_merge_strategy": "replace", "nest_key": "nest_value"},
            }
        }
        pong_route.scenario_attributes = {"json": {"data3": "value3"}}
        pong_route.for_scenario("pong").post()
        expected_merged_args = {
            "method": "post",
            "json": {
                "data1": "value1",
                "data2": "value2",
                "data3": "value3",
                "nested_key1": {"nest_key": "nest_value"},
            },
            "url": f"{VerifyRoute.BASE_URL}/pong",
        }
        assert mock_request.call_args.kwargs == expected_merged_args

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_merge_remove(self, mock_request, pong_route):
        pong_route.route_attributes = {
            "json": {"data1": "value1", "nested_key1": {"data1": "value1"}}
        }
        pong_route.method_attributes = {
            "json": {"data2": "value2", "nested_key1": {"_merge_strategy": "remove"}}
        }
        pong_route.scenario_attributes = {"json": {"data3": "value3"}}

        pong_route.for_scenario("pong").post()
        expected_merged_args = {
            "method": "post",
            "json": {"data1": "value1", "data2": "value2", "data3": "value3"},
            "url": f"{VerifyRoute.BASE_URL}/pong",
        }
        assert mock_request.call_args.kwargs == expected_merged_args

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_nested_multi_merge(self, mock_request, pong_route):
        pong_route.route_attributes = {
            "json": {"data": "value", "json_key1": {"data1": "value1"}}
        }
        pong_route.method_attributes = {
            "json": {
                "json_key1": {"d2": "value"},
                "nest2": {
                    "nest3": {"json_nested_key3": {"k1": "v1"}},
                    "nest3_1": {"json_nested_key3_1": "values"},
                    "nest4": {"json_nested_key4": {"k1": "v1"}},
                },
            }
        }
        pong_route.scenario_attributes = {
            "json": {
                "json_key1": {"d3": "value"},
                "nest2": {
                    "nest3": {
                        "json_nested_key3": {"_merge_strategy": "replace", "k2": "v2"}
                    },
                    "nest4": {
                        "json_nested_key4": {
                            "_merge_strategy": "deep_merge",
                            "k2": "v2",
                        }
                    },
                    "nest3_1": {"_merge_strategy": "remove"},
                },
            }
        }

        pong_route.for_scenario("pong").post()

        expected_merged_args = {
            "method": "post",
            "url": f"{VerifyRoute.BASE_URL}/pong",
            "json": {
                "data": "value",
                "json_key1": {"data1": "value1", "d2": "value", "d3": "value"},
                "nest2": {
                    "nest3": {"json_nested_key3": {"k2": "v2"}},
                    "nest4": {"json_nested_key4": {"k1": "v1", "k2": "v2"}},
                },
            },
        }

        assert mock_request.call_args.kwargs == expected_merged_args

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_invalid_merge_strategy(self, mock_request, pong_route):
        pong_route.route_attributes = {
            "params": {"data1": "value1", "nested_key1": {"data1": "value1"}}
        }
        pong_route.method_attributes = {
            "params": {"data2": "value2", "nested_key1": {"_merge_strategy": "pop"}}
        }
        with pytest.raises(ValueError):
            pong_route.for_scenario("pong").get()

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_attribute_dictionary(self, mock_request):
        route = GroupPongRoute()
        route.for_scenario("with_leap_year_dob").get()
        expected_merged_args = {
            "method": "get",
            "params": {
                "username": "John Doe",
                "id": 3149232,
                "firstname": "John",
                "lastname": "Doe",
                "userDetails": {"DOB": "29/02/1996"},
            },
            "url": f"{VerifyRoute.BASE_URL}/pong",
        }
        assert mock_request.call_args.kwargs == expected_merged_args

    @patch("requests.request", side_effect=mock_request_side_effect)
    def test_with_scenario_group(self, mock_request):
        route = GroupPongRoute()
        scenario_route = route.for_scenario(
            "group_scenario", group_name="pong_scenario"
        )
        scenario_route.get()
        expected_merged_args = {
            "method": "get",
            "params": {
                "firstname": "John",
                "lastname": "Doe",
                "username": "John Doe",
                "id": 3149232,
                "userDetails": {"DOB": "01/01/2011"},
            },
            "url": f"{VerifyRoute.BASE_URL}/pong",
        }
        assert (
            route.scenario_method.__self__.route == route
        ), "scenario group should get route reference assigned"
        assert (
            mock_request.call_args.kwargs == expected_merged_args
        ), "merged request args does not match"
