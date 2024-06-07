import httpx
import pytest
from beaver_routes.core.response import Response


def test_status_code(response):
    """Test the status_code property."""
    assert response.status_code == 200

def test_headers(response):
    """Test the headers property."""
    expected_headers = {"Content-Type": "application/json"}
    actual_headers = {k.lower(): v for k, v in response.headers.items()}
    expected_headers_lower = {k.lower(): v for k, v in expected_headers.items()}
    for key, value in expected_headers_lower.items():
        assert actual_headers[key] == value

def test_cookies(response):
    """Test the cookies property."""
    assert response.cookies == {"session_id": "abc123"}

def test_url(response):
    """Test the url property."""
    assert response.url == "https://example.com"

def test_content(response):
    """Test the content property."""
    assert response.content == b'{"key": "value"}'

def test_text(response):
    """Test the text property."""
    assert response.text == '{"key": "value"}'

def test_json_content(response):
    """Test the json_content property."""
    assert response.json_content == {"key": "value"}

def test_getattr(response):
    """Test __getattr__ method."""
    assert response.reason_phrase == "OK"
    assert response.is_success

if __name__ == "__main__":
    pytest.main()
