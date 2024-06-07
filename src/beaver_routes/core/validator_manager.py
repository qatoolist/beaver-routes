from typing import Any, List, Type

from beaver_routes.validators.base import Validator
from beaver_routes.exceptions.exceptions import ValidationError

class ValidatorManager:
    def __init__(self) -> None:
        self.validators: List[Validator] = []
        self.enabled = True

    def add_validator(self, validator_cls: Type[Validator]) -> None:
        self.validators.append(validator_cls())

    def apply_validators(self, response: Any) -> None:
        if self.enabled:
            for validator in self.validators:
                validator.validate(response)
