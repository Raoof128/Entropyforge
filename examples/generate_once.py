#!/usr/bin/env python3
"""Minimal example: generate values using crypto_core without the GUI."""

from __future__ import annotations

from entropyforge.crypto_core import (
    generate_alphanumeric,
    generate_hex_key,
    generate_secure_int_inclusive,
)


def main() -> None:
    pw = generate_alphanumeric(16)
    hx = generate_hex_key(8)
    n = generate_secure_int_inclusive(1, 100)
    print("alphanumeric (16):", pw)
    print("hex (8 bytes):", hx)
    print("integer [1,100]:", n)


if __name__ == "__main__":
    main()
