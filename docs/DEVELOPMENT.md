# Development guide

## Prerequisites

- Python 3.11 or newer
- Git

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Commands

See the [Makefile](../Makefile) for shortcuts:

| Target | Action |
|--------|--------|
| `make install` | Editable install with dev extras |
| `make format` | Ruff formatter |
| `make lint` | Ruff linter |
| `make test` | Pytest with coverage |
| `make check` | Format check + lint + tests |

## Pre-commit (optional)

```bash
pip install pre-commit
pre-commit install
```

Runs Ruff lint + format on commit.

## VS Code / Dev Container

Open the folder in VS Code and “Reopen in Container” if using
`.devcontainer/devcontainer.json`.

## Adding a locale

1. Copy `src/entropyforge/locales/en.json` to a new file (e.g. `de.json`).
2. Translate values; keep keys identical.
3. Add the locale code to the Settings option menu in `ui.py` if exposed in UI.

## CI parity

GitHub Actions runs Ruff (check + format check), pytest, and optional PyInstaller
builds. Match those commands locally before pushing.
