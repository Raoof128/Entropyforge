# EntropyForge

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Desktop application for **cryptographically secure** passwords, hex keys, and uniform integers. Generation uses Python’s [`secrets`](https://docs.python.org/3/library/secrets.html) module (OS-backed CSPRNG), not the Mersenne Twister `random` module.

## Contents

- [Features](#features)
- [Quick start](#quick-start)
- [Documentation](#documentation)
- [Development](#development)
- [Quality gates](#quality-gates)
- [Packaging](#packaging)
- [Community](#community)
- [Project layout](#project-layout)
- [License](#license)

## Features

- **CSPRNG:** `secrets` / `os.urandom` only for generation logic (stdlib).
- **UI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — mode radios with stable internal IDs, presets, output toolbar (clear, regenerate, mask), entropy bar and hints, responsive entropy row below ~480px width.
- **i18n:** JSON locales (`en`, `ar`) merged at runtime; add files under `src/entropyforge/locales/`. Arabic uses mirrored **RTL chrome** (pack/grid order); restart after changing language to reload UI.
- **Settings:** Language, high-contrast theme, paranoid confirmations for large outputs, optional clipboard auto-clear — stored under the OS config directory via [`platformdirs`](https://pypi.org/project/platformdirs/).
- **Logging:** Warnings and errors to `entropyforge.log` beside settings (no secrets logged).
- **Tests:** `pytest`, `ruff`, optional `hypothesis` property tests; GitHub Actions CI (lint, format, tests with coverage, PyInstaller onedir on Linux).

## Quick start

```bash
cd EntropyForge
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
entropyforge
# or: python -m entropyforge
```

Editable install is required so `entropyforge` resolves the package under `src/`.

## Documentation

| Resource | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Components and data flow |
| [docs/API.md](docs/API.md) | Public modules and entry points |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Local setup, Makefile, pre-commit, dev container |
| [docs/PACKAGING.md](docs/PACKAGING.md) | PyInstaller, CI artifacts, signing pointers |
| [examples/README.md](examples/README.md) | Non-GUI usage example |

## Development

```bash
pip install -e ".[dev]"
# or: make install
make check    # format-check + lint + pytest with coverage
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for `.pre-commit-config.yaml`, `.devcontainer/`, and editor settings.

## Quality gates

| Command | Purpose |
|---------|---------|
| `ruff format src tests` | Format |
| `ruff format --check src tests` | CI-style format check |
| `ruff check src tests` | Lint |
| `pytest tests/ -v --cov=entropyforge --cov-report=term-missing` | Tests + coverage (`ui.py` and `__main__.py` omitted from coverage; see `pyproject.toml`) |

## Packaging (PyInstaller)

```bash
pip install pyinstaller
pyinstaller entropyforge.spec
# or a one-folder bundle (often faster cold start):
pyinstaller entropyforge_onedir.spec
```

See [docs/PACKAGING.md](docs/PACKAGING.md) for one-file vs one-folder, CI artifacts, and documentation-only notes on macOS notarization and Windows Authenticode.

**Lockfile:** `requirements-lock.txt` (from `pip freeze` after a clean install). Pin CI and releases against it when you need reproducibility.

## Community

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards (Contributor Covenant 2.1) |
| [SECURITY.md](SECURITY.md) | Reporting vulnerabilities |
| [CHANGELOG.md](CHANGELOG.md) | Project history |

## Project layout

```text
EntropyForge/
├── pyproject.toml
├── requirements.txt
├── requirements-lock.txt
├── Makefile
├── entropyforge.spec
├── entropyforge_onedir.spec
├── docs/
├── examples/
├── src/entropyforge/
│   ├── main.py
│   ├── ui.py
│   ├── crypto_core.py
│   ├── config.py
│   ├── logging_config.py
│   ├── i18n.py
│   └── locales/
└── tests/
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
