from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from entropyforge import main as main_mod


def test_main_invokes_run_app(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    mock_run = MagicMock()
    monkeypatch.setattr(main_mod, "run_app", mock_run)
    monkeypatch.setattr(main_mod, "config_directory", lambda: tmp_path)
    monkeypatch.setattr(main_mod, "load_settings", lambda: {"locale": "en"})
    monkeypatch.setattr(main_mod, "setup_logging", lambda _p: None)
    monkeypatch.setattr(main_mod, "load_locale", lambda _l: None)

    main_mod.main()

    mock_run.assert_called_once()
    assert mock_run.call_args[0][0]["locale"] == "en"


def test_main_reraises_after_logging_exception(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def boom(_settings: dict[str, Any]) -> None:
        msg = "simulated UI failure"
        raise RuntimeError(msg)

    monkeypatch.setattr(main_mod, "run_app", boom)
    monkeypatch.setattr(main_mod, "config_directory", lambda: tmp_path)
    monkeypatch.setattr(main_mod, "load_settings", lambda: {"locale": "en"})
    monkeypatch.setattr(main_mod, "setup_logging", lambda _p: None)
    monkeypatch.setattr(main_mod, "load_locale", lambda _l: None)

    with pytest.raises(RuntimeError, match="simulated UI failure"):
        main_mod.main()
