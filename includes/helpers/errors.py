from rest_framework.exceptions import ValidationError


class InvalidInputError(ValidationError):
    status_code = 400,
    default_detail = "Invalid input provided",
    default_code = "invalid_input"