"""Validators"""

import logging

_LOGGER = logging.getLogger(__name__)


class ValidationError(Exception):
    """Input validation error"""


__all__ = ["int_validator", "float_validator", "all_digits_validator"]


def int_validator(value) -> int:
    try:
        converted = int(value)
    except ValueError:
        raise ValidationError("Not a valid integer.")
    if value == str(converted):
        return converted
    raise ValidationError("not a valid integer.")


def float_validator(value) -> float:
    try:
        converted = float(value)
    except ValueError:
        raise ValidationError("Not a valid float.")
    if converted == 0.0:
        return converted
    if value == str(converted):
        return converted
    raise ValidationError("not a valid float.")


def all_digits_validator(value) -> str:
    if value.isdigit():
        return value
    raise ValidationError("Only numbers are allowed.")
