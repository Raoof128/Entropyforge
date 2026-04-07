# -------------------------------------------------------------------------- //
# FILE LOGGING (NO SECRETS) //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(config_dir: Path) -> None:
    log_path = config_dir / "entropyforge.log"
    root = logging.getLogger("entropyforge")
    root.setLevel(logging.DEBUG)
    if root.handlers:
        return
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.WARNING)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"),
    )
    root.addHandler(handler)
