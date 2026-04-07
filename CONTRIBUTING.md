# Contributing to EntropyForge

Thank you for your interest in improving EntropyForge. This document explains
how to set up a development environment, run checks, and submit changes.

## Code of conduct

All participants must follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Development setup

```bash
git clone <repository-url>
cd EntropyForge
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Optional: use the [VS Code Dev Container](.devcontainer/devcontainer.json) for
a consistent environment.

## Quality bar

Before opening a PR:

```bash
make check          # or: see Makefile targets
# equivalent:
ruff format --check src tests
ruff check src tests
pytest tests/ -v --cov=entropyforge --cov-report=term-missing
```

- **Ruff** enforces style and common bug patterns; run `ruff format src tests` to
  auto-format.
- **Pytest** with coverage helps catch regressions in `crypto_core` and i18n
  tests.
- User-visible strings belong in `src/entropyforge/locales/*.json`, not
  hardcoded in Python (see existing keys).

## Project layout

| Path | Role |
|------|------|
| `src/entropyforge/crypto_core.py` | CSPRNG and parsing (stdlib `secrets` only) |
| `src/entropyforge/ui.py` | CustomTkinter UI (no crypto logic) |
| `src/entropyforge/i18n.py` | Locale loading and `t()` |
| `src/entropyforge/config.py` | User settings JSON via `platformdirs` |
| `tests/` | Pytest suite (unit, property, locale coverage) |

Architecture overview: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Pull requests

1. **Branch** from `main` with a descriptive name (`fix/parse-edge-case`,
   `feature/locale-fr`).
2. **Describe** the change, motivation, and testing performed.
3. **Keep diffs focused**—avoid unrelated refactors in the same PR.
4. **Update docs** if behavior, configuration, or packaging changes.

## Reporting bugs

Use the issue templates under `.github/ISSUE_TEMPLATE/`. Include OS, Python
version, and steps to reproduce.

## Security

See [SECURITY.md](SECURITY.md) for responsible disclosure.
