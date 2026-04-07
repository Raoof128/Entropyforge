from __future__ import annotations

import json
from pathlib import Path

import pytest

import entropyforge.config as cfg


def test_load_returns_defaults_when_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(cfg, "settings_path", lambda: tmp_path / "settings.json")
    assert cfg.load_settings() == cfg.DEFAULT_SETTINGS.copy()


def test_save_and_load_roundtrip(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    monkeypatch.setattr(cfg, "settings_path", lambda: path)
    data = cfg.DEFAULT_SETTINGS.copy()
    data["locale"] = "ar"
    cfg.save_settings(data)
    loaded = cfg.load_settings()
    assert loaded["locale"] == "ar"
    assert json.loads(path.read_text(encoding="utf-8"))["locale"] == "ar"


def test_config_directory_creates_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    target = tmp_path / "entropyforge_cfg"
    monkeypatch.setattr(
        "entropyforge.config.user_config_dir",
        lambda _app, appauthor=False: str(target),
    )
    result = cfg.config_directory()
    assert result == target
    assert result.is_dir()
