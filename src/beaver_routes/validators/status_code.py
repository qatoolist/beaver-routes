from typing import Any

from beaver_routes.validators.base import Validator
from beaver_routes.exceptions.exceptions import ValidationError

class StatusCodeValidator(Validator):
    def __init__(self, expected_status: int):
        self.expected_status = expected_status

    def validate(self, response: Any) -> None:
        if response.status_code != self.expected_status:
            raise ValidationError(f"Expected status {self.expected_status}, got {response.status_code}")
