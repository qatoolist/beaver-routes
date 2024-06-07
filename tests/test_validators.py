# tests/test_validators.py
import pytest

from beaver_routes.validators.status_code import StatusCodeValidator
from beaver_routes.validators.headers import HeaderValidator
from beaver_routes.exceptions.exceptions import ValidationError
from beaver_routes.core.response import Response

def test_status_code_validator_pass(mock_response):
    response = Response(mock_response)
    validator = StatusCodeValidator(200)
    validator.validate(response)  # Should pass without exception

def test_status_code_validator_fail(mock_response):
    response = Response(mock_response)
    validator = StatusCodeValidator(404)
    with pytest.raises(ValidationError):
        validator.validate(response)  # Should raise ValidationError

def test_header_validator_pass(mock_response):
    response = Response(mock_response)
    validator = HeaderValidator({"Content-Type": "application/json"})
    validator.validate(response)  # Should pass without exception

def test_header_validator_fail(mock_response):
    response = Response(mock_response)
    validator = HeaderValidator({"Content-Type": "text/html"})
    with pytest.raises(ValidationError):
        validator.validate(response)  # Should raise ValidationError

if __name__ == "__main__":
    pytest.main()
