# -------------------------------------------------------------------------- //
# CRYPTO CORE — OS ENTROPY VIA secrets (NO Mersenne Twister) //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import math
import secrets
import string
from typing import Final

_ALPHANUMERIC: Final[str] = string.ascii_letters + string.digits

MAX_ALPHANUMERIC_LENGTH: Final[int] = 4096
MAX_HEX_BYTES: Final[int] = 512

PARANOID_FRACTION: Final[float] = 0.85
PARANOID_RANGE_SPAN: Final[int] = 10**12


class CryptoCoreError(ValueError):
    """Validation or generation error with a string key for UI messaging."""

    def __init__(self, message_key: str) -> None:
        super().__init__(message_key)
        self.message_key = message_key


def _digits_only_decimal_int(raw: str) -> int:
    s = raw.strip()
    if not s:
        raise CryptoCoreError("error.range_parse")
    if s[0] in "+-":
        sign = -1 if s[0] == "-" else 1
        body = s[1:]
    else:
        sign = 1
        body = s
    if not body.isascii() or not body.isdigit():
        raise CryptoCoreError("error.range_parse")
    return sign * int(body)


def parse_strict_int(raw: str) -> int:
    return _digits_only_decimal_int(raw)


def parse_positive_int(raw: str, *, error_key: str) -> int:
    value = _digits_only_decimal_int(raw)
    if value < 1:
        raise CryptoCoreError(error_key)
    return value


def validate_int_range(min_value: int, max_value: int) -> None:
    if min_value >= max_value:
        raise CryptoCoreError("error.range_min_max")


def generate_secure_int_inclusive(min_value: int, max_value: int) -> int:
    validate_int_range(min_value, max_value)
    span = max_value - min_value + 1
    return min_value + secrets.randbelow(span)


def generate_alphanumeric(length: int) -> str:
    if length < 1:
        raise CryptoCoreError("error.length_invalid")
    if length > MAX_ALPHANUMERIC_LENGTH:
        raise CryptoCoreError("error.password_length_limit")
    alphabet = _ALPHANUMERIC
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_hex_key(num_bytes: int) -> str:
    if num_bytes < 1:
        raise CryptoCoreError("error.hex_bytes_invalid")
    if num_bytes > MAX_HEX_BYTES:
        raise CryptoCoreError("error.hex_bytes_limit")
    return secrets.token_hex(num_bytes)


def entropy_bits_uniform_range(*, count: int) -> float:
    if count < 2:
        return 0.0
    return math.log2(count)


def entropy_bits_alphanumeric(*, length: int) -> float:
    if length < 1:
        return 0.0
    return length * math.log2(len(_ALPHANUMERIC))


def entropy_bits_hex_key(*, num_bytes: int) -> float:
    if num_bytes < 1:
        return 0.0
    return num_bytes * 8.0


def paranoid_password_length(length: int) -> bool:
    return length > int(MAX_ALPHANUMERIC_LENGTH * PARANOID_FRACTION)


def paranoid_hex_bytes(num_bytes: int) -> bool:
    return num_bytes > int(MAX_HEX_BYTES * PARANOID_FRACTION)


def paranoid_integer_range(lo: int, hi: int) -> bool:
    if lo >= hi:
        return False
    span = hi - lo + 1
    return span > PARANOID_RANGE_SPAN
