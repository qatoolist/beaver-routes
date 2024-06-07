# src/beaver_routes/validators/headers.py
from typing import Any, Dict

from beaver_routes.validators.base import Validator
from beaver_routes.exceptions.exceptions import ValidationError

class HeaderValidator(Validator):
    def __init__(self, expected_headers: Dict[str, str]):
        self.expected_headers = expected_headers

    def validate(self, response: Any) -> None:
        for key, value in self.expected_headers.items():
            if response.headers.get(key) != value:
                raise ValidationError(f"Expected header {key}: {value}, got {response.headers.get(key)}")
