"""
validators.py
Reusable input validation helpers -- keeps validation logic out of the CLI
and business-logic modules (supports Maintainability & Usability).
"""


class ValidationError(Exception):
    """Raised when user-supplied input fails validation."""
    pass


def validate_non_empty_string(value: str, field_name: str = "value") -> str:
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return str(value).strip()


def validate_positive_float(value, field_name: str = "value") -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a number.")
    if number < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return number


def validate_positive_int(value, field_name: str = "value") -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a whole number.")
    if number < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return number


def validate_menu_choice(value: str, valid_choices: set, field_name: str = "choice") -> str:
    value = str(value).strip()
    if value not in valid_choices:
        raise ValidationError(
            f"Invalid {field_name}. Expected one of: {', '.join(sorted(valid_choices))}"
        )
    return value
