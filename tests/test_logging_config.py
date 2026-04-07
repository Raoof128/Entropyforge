from __future__ import annotations

from pathlib import Path

from entropyforge.logging_config import setup_logging


def test_setup_logging_idempotent(tmp_path: Path) -> None:
    setup_logging(tmp_path)
    setup_logging(tmp_path)
    assert (tmp_path / "entropyforge.log").is_file()
