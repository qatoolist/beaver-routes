
from typing import Any

class Validator:
    def validate(self, response: Any) -> None:
        """Validate the given response.

        Args:
            response (Any): The response to validate.

        Raises:
            ValidationError: If the validation fails.
        """
        raise NotImplementedError("Validator subclasses must implement validate method")
