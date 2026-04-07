# -------------------------------------------------------------------------- //
# LOCALE COVERAGE — crypto_core CryptoCoreError LITERALS //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import ast
import json
from pathlib import Path


def _crypto_core_error_literal_keys() -> set[str]:
    path = Path(__file__).resolve().parents[1] / "src" / "entropyforge" / "crypto_core.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    keys: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_Raise(self, node: ast.Raise) -> None:
            exc = node.exc
            if not isinstance(exc, ast.Call) or not exc.args:
                return
            func = exc.func
            arg0 = exc.args[0]
            if (
                isinstance(func, ast.Name)
                and func.id == "CryptoCoreError"
                and isinstance(arg0, ast.Constant)
                and isinstance(arg0.value, str)
            ):
                keys.add(arg0.value)

    Visitor().visit(tree)
    return keys


def test_all_crypto_core_error_literals_exist_in_en_json() -> None:
    en_path = Path(__file__).resolve().parents[1] / "src" / "entropyforge" / "locales" / "en.json"
    en_keys = set(json.loads(en_path.read_text(encoding="utf-8")).keys())
    code_keys = _crypto_core_error_literal_keys()
    missing = code_keys - en_keys
    assert not missing, f"Missing from en.json: {sorted(missing)}"


def test_is_rtl_matches_locale() -> None:
    from entropyforge.i18n import is_rtl, load_locale

    load_locale("en")
    assert not is_rtl()
    load_locale("ar")
    assert is_rtl()
    load_locale("en")
