from unittest.mock import patch

import pytest

from tests.mock.mock_requests import mock_request_side_effect
from tests.mock_routes import VerifyRoute


class TestRouteMethod:
    @pytest.fixture
    def verify_route(self):
        return VerifyRoute()

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_get(self, mock_request, verify_route):
        response = verify_route.get()

        assert response.status_code == 400
        assert response.json() == {"message": "missing parameter key"}

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_options(self, mock_request, verify_route):
        response = verify_route.options()

        assert response.status_code == 200
        assert response.headers['Allow'] == 'OPTIONS, GET, HEAD, POST, PUT, PATCH'

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_head(self, mock_request, verify_route):
        response = verify_route.head()
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_post(self, mock_request, verify_route):
        response = verify_route.post(data={'key': 'value'})
        assert response.status_code == 201
        assert response.json() == {"message": "post request processed"}

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_put(self, mock_request, verify_route):
        response = verify_route.put(data={'key': 'value'})
        assert response.status_code == 200
        assert response.json() == {"message": "put request processed"}

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_patch(self, mock_request, verify_route):
        response = verify_route.patch(data={'key': 'value'})
        assert response.status_code == 200
        assert response.json() == {"message": "patch request processed"}

    @patch('requests.request', side_effect=mock_request_side_effect)
    def test_delete(self, mock_request, verify_route):
        response = verify_route.delete()
        assert response.status_code == 200
        assert response.json() == {"message": "delete request processed"}
