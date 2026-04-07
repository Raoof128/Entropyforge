# -------------------------------------------------------------------------- //
# CRYPTO CORE TESTS //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import math

import pytest

from entropyforge.crypto_core import (
    MAX_ALPHANUMERIC_LENGTH,
    MAX_HEX_BYTES,
    CryptoCoreError,
    entropy_bits_alphanumeric,
    entropy_bits_hex_key,
    entropy_bits_uniform_range,
    generate_alphanumeric,
    generate_hex_key,
    generate_secure_int_inclusive,
    parse_positive_int,
    parse_strict_int,
)
from entropyforge.i18n import t


def test_parse_strict_int_accepts_decimal_integers() -> None:
    assert parse_strict_int(" 42 ") == 42
    assert parse_strict_int("-7") == -7


def test_parse_strict_int_rejects_float_like() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        parse_strict_int("3.14")
    assert exc.value.message_key == "error.range_parse"


def test_parse_strict_int_rejects_unicode_digit_char() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        parse_strict_int("²")
    assert exc.value.message_key == "error.range_parse"


def test_parse_strict_int_rejects_empty() -> None:
    with pytest.raises(CryptoCoreError):
        parse_strict_int("   ")


def test_generate_int_in_range() -> None:
    for _ in range(200):
        value = generate_secure_int_inclusive(1, 10_000)
        assert 1 <= value <= 10_000


def test_generate_int_rejects_invalid_range() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        generate_secure_int_inclusive(5, 5)
    assert exc.value.message_key == "error.range_min_max"


def test_alphanumeric_length_and_charset() -> None:
    s = generate_alphanumeric(32)
    assert len(s) == 32
    assert all(c.isalnum() for c in s)


def test_alphanumeric_rejects_non_positive_length() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        generate_alphanumeric(0)
    assert exc.value.message_key == "error.length_invalid"


def test_hex_key_length() -> None:
    h = generate_hex_key(8)
    assert len(h) == 16
    assert all(c in "0123456789abcdef" for c in h)


def test_hex_key_rejects_zero_bytes() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        generate_hex_key(0)
    assert exc.value.message_key == "error.hex_bytes_invalid"


def test_entropy_uniform_range() -> None:
    assert entropy_bits_uniform_range(count=2) == pytest.approx(1.0)
    assert entropy_bits_uniform_range(count=1024) == pytest.approx(math.log2(1024))


def test_entropy_alphanumeric() -> None:
    bits = entropy_bits_alphanumeric(length=10)
    assert bits == pytest.approx(10 * math.log2(62))


def test_entropy_hex() -> None:
    assert entropy_bits_hex_key(num_bytes=2) == 16.0


def test_parse_positive_int() -> None:
    assert parse_positive_int("8", error_key="error.length_invalid") == 8


def test_parse_positive_int_rejects_zero() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        parse_positive_int("0", error_key="error.length_invalid")
    assert exc.value.message_key == "error.length_invalid"


def test_parse_strict_int_rejects_lone_sign() -> None:
    with pytest.raises(CryptoCoreError) as exc:
        parse_strict_int("+")
    assert exc.value.message_key == "error.range_parse"


def test_entropy_uniform_range_single_outcome() -> None:
    assert entropy_bits_uniform_range(count=1) == 0.0


def test_alphanumeric_respects_max_length() -> None:
    generate_alphanumeric(MAX_ALPHANUMERIC_LENGTH)
    with pytest.raises(CryptoCoreError) as exc:
        generate_alphanumeric(MAX_ALPHANUMERIC_LENGTH + 1)
    assert exc.value.message_key == "error.password_length_limit"


def test_hex_respects_max_bytes() -> None:
    generate_hex_key(MAX_HEX_BYTES)
    with pytest.raises(CryptoCoreError) as exc:
        generate_hex_key(MAX_HEX_BYTES + 1)
    assert exc.value.message_key == "error.hex_bytes_limit"


def test_all_crypto_core_error_keys_exist_in_strings() -> None:
    keys = {
        "error.hex_bytes_invalid",
        "error.hex_bytes_limit",
        "error.length_invalid",
        "error.password_length_limit",
        "error.range_min_max",
        "error.range_parse",
        "error.unexpected",
    }
    for key in keys:
        assert t(key) != key, f"missing i18n string: {key}"
