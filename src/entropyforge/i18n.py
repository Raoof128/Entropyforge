# -------------------------------------------------------------------------- //
# I18N — LOAD JSON LOCALES //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import json
from pathlib import Path
from typing import Final

_FALLBACK_LOCALE: Final[str] = "en"

# Locales that use right-to-left chrome (mirrored layout in ui.py).
_RTL_LOCALES: Final[frozenset[str]] = frozenset({"ar", "he", "fa", "ur"})

_strings: dict[str, str] = {}
_current_locale: str = _FALLBACK_LOCALE


def _locale_dir() -> Path:
    return Path(__file__).resolve().parent / "locales"


def _load_locale_file(locale: str) -> dict[str, str]:
    path = _locale_dir() / f"{locale}.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_locale(locale: str) -> None:
    """Load merged strings: English base, then overlay for `locale`."""
    global _current_locale, _strings
    _current_locale = locale
    base = _load_locale_file(_FALLBACK_LOCALE)
    if locale != _FALLBACK_LOCALE:
        overlay = _load_locale_file(locale)
        merged = {**base, **overlay}
    else:
        merged = dict(base)
    _strings = merged


def t(key: str) -> str:
    return _strings.get(key, key)


def known_keys() -> frozenset[str]:
    return frozenset(_strings.keys())


def current_locale() -> str:
    return _current_locale


def is_rtl() -> bool:
    return _current_locale in _RTL_LOCALES
