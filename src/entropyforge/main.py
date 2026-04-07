# -------------------------------------------------------------------------- //
# ENTRY POINT //
# -------------------------------------------------------------------------- //

from __future__ import annotations

import logging

from entropyforge.config import config_directory, load_settings
from entropyforge.i18n import load_locale
from entropyforge.logging_config import setup_logging
from entropyforge.ui import run_app

logger = logging.getLogger("entropyforge")


def main() -> None:
    cfg_dir = config_directory()
    setup_logging(cfg_dir)
    settings = load_settings()
    load_locale(str(settings.get("locale", "en")))
    try:
        run_app(settings)
    except Exception:
        logger.exception("Application failed")
        raise
