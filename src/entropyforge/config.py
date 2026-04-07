# -------------------------------------------------------------------------- //
# USER CONFIG (JSON ON DISK) //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from platformdirs import user_config_dir


def config_directory() -> Path:
    path = Path(user_config_dir("entropyforge", appauthor=False))
    path.mkdir(parents=True, exist_ok=True)
    return path


def settings_path() -> Path:
    return config_directory() / "settings.json"


DEFAULT_SETTINGS: dict[str, Any] = {
    "clipboard_clear_seconds": 0,
    "first_run_banner_dismissed": False,
    "high_contrast": False,
    "locale": "en",
    "paranoid_confirm": True,
}


def load_settings() -> dict[str, Any]:
    path = settings_path()
    if not path.is_file():
        return DEFAULT_SETTINGS.copy()
    raw = json.loads(path.read_text(encoding="utf-8"))
    merged = DEFAULT_SETTINGS.copy()
    merged.update(raw)
    return merged


def save_settings(settings: dict[str, Any]) -> None:
    path = settings_path()
    path.write_text(json.dumps(settings, indent=2, sort_keys=True) + "\n", encoding="utf-8")
