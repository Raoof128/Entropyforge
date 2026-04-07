from __future__ import annotations

import pytest

from entropyforge.i18n import load_locale


@pytest.fixture(scope="session", autouse=True)
def _load_en_locale() -> None:
    load_locale("en")
