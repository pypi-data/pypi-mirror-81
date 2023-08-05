"""Validators"""

# todo: Rethink this.

import logging

from pydantic.decorator import validate_arguments
from pydantic.errors import NotDigitError

_LOGGER = logging.getLogger(__name__)

# pylint: disable=invalid-name,no-self-use


__all__ = ["int_validator", "float_validator", "all_digits_validator"]


@validate_arguments
def int_validator(value: int) -> int:
    return value


@validate_arguments
def float_validator(value: float) -> float:
    return value


class AllDigits(str):
    def __init__(self, value):
        self.value = value

    @classmethod
    def validate_digits(cls, value) -> str:
        if not value.isdigit():
            raise NotDigitError
        return value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_digits


@validate_arguments
def all_digits_validator(value: AllDigits) -> str:
    return value
