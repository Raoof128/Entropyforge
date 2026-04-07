# -------------------------------------------------------------------------- //
# SMOKE IMPORTS //
# -------------------------------------------------------------------------- //

from __future__ import annotations


def test_import_entropyforge_package() -> None:
    import entropyforge

    assert entropyforge.__version__


def test_import_crypto_and_i18n() -> None:
    from entropyforge import crypto_core, i18n  # noqa: F401


def test_import_ui_module() -> None:
    from entropyforge import ui  # noqa: F401
