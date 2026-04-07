# -------------------------------------------------------------------------- //
# PROPERTY-BASED TESTS (HYPOTHESIS) //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import contextlib

from hypothesis import given
from hypothesis import strategies as st

from entropyforge.crypto_core import (
    CryptoCoreError,
    generate_secure_int_inclusive,
    parse_strict_int,
)


@given(st.text())
def test_parse_strict_int_never_raises_unexpected(s: str) -> None:
    with contextlib.suppress(CryptoCoreError):
        parse_strict_int(s)


@given(st.integers(1, 500), st.integers(1, 500))
def test_rand_int_in_range(a: int, b: int) -> None:
    lo = min(a, b)
    hi = max(a, b)
    if lo == hi:
        return
    v = generate_secure_int_inclusive(lo, hi)
    assert lo <= v <= hi
