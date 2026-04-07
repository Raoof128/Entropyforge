# Changelog

## Raouf: 2026-04-07 — Canonical GitHub URLs (Raoof128)
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Package metadata alignment with GitHub
- **Summary:** Updated `[project.urls]` and changelog copy to use canonical `https://github.com/Raoof128/entropyforge` (matching the live remote).
- **Files changed:** `pyproject.toml`, `AGENT.md`, `CHANGELOG.md`
- **Verification:** `git push` to `origin main`
- **Follow-ups:** None

## Raouf: 2026-04-07 — Remove Dependabot; publish to GitHub
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Repository hosting
- **Summary:** Removed GitHub Dependabot configuration; project URLs point at `https://github.com/Raoof128/entropyforge`; `.hypothesis/` ignored; source published as a public repository under `Raoof128`.
- **Files changed:** `.github/dependabot.yml` (removed), `.gitignore`, `pyproject.toml`, `README.md`, `AGENT.md`, `CHANGELOG.md`
- **Verification:** Remote push to `origin` on GitHub.
- **Follow-ups:** None.

## Raouf: 2026-04-07 — Production audit: docs, governance, tests, CI
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Industry-facing audit — coverage threshold, config/main/logging tests, README and CI alignment
- **Summary:** Added unit tests for `config` (including `config_directory`), `logging_config`, and `main` (success path and logged exception re-raise); CI runs Ruff format check, Ruff lint, and pytest with coverage; README expanded with documentation index, community links, quality gates, and placeholder repository URL note; documentation index links to `examples/`.
- **Files changed:** `README.md`, `.github/workflows/ci.yml`, `docs/README.md`, `tests/test_config.py`, `tests/test_logging_config.py`, `tests/test_main.py`, `AGENT.md`, `CHANGELOG.md`
- **Verification:** `ruff format --check src tests`; `ruff check src tests`; `pytest tests/ -v --cov=entropyforge` → 33 passed, coverage meets `fail_under` (88%).
- **Follow-ups:** Replace placeholder GitHub URLs in `pyproject.toml` when publishing; optional Codecov or similar in CI.

## Raouf: 2026-04-07 — Follow-ups: RTL, PyInstaller onedir, locale tests, packaging docs
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Optional follow-ups from prior roadmap
- **Summary:** RTL mirrored chrome for `i18n.is_rtl()` locales (`ar`, `he`, `fa`, `ur`); `entropyforge_onedir.spec` + CI job uploading Linux onedir artifact; AST test ensuring every literal `CryptoCoreError("…")` in `crypto_core.py` exists in `locales/en.json`; `docs/PACKAGING.md` for notarization/signing (documentation only); README/AGENT updates.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `.github/workflows/ci.yml`, `docs/PACKAGING.md`, `entropyforge_onedir.spec`, `src/entropyforge/i18n.py`, `src/entropyforge/ui.py`, `tests/test_crypto_core_locale_keys.py`
- **Verification:** `pytest tests/ -v` → 27 passed; `ruff check src tests`
- **Follow-ups:** macOS/Windows PyInstaller builds on native runners if you ship desktop binaries.

## Raouf: 2026-04-07 — Feature pack: i18n, settings, CI, packaging
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** EntropyForge “add all” improvements (locales EN/AR, presets, output tools, paranoid dialogs, clipboard timer, first-run banner, logging, `pyproject.toml` + `entropyforge` console script, CI, ruff, hypothesis, PyInstaller spec, lockfile, strict ASCII integer parsing fix).
- **Files changed:** `pyproject.toml`, `requirements.txt`, `requirements-lock.txt`, `entropyforge.spec`, `.github/workflows/ci.yml`, `README.md`, `AGENT.md`, `CHANGELOG.md`, `.gitignore`, `src/entropyforge/*` (new package), `tests/*`; removed flat `src/main.py`, `src/ui.py`, `src/crypto_core.py`, `src/strings.py`, `src/__init__.py`.
- **Verification:** `pip install -e ".[dev]"`; `pytest tests/ -v` (25 tests); `ruff check src tests`; `python -c` Arabic `load_locale('ar')`.
- **Follow-ups:** Optional one-dir PyInstaller bundle; stronger RTL layout for Arabic; automated locale coverage tests.

## Raouf: 2026-04-07 — Audit: UI/UX
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** EntropyForge interface and experience
- **Summary:** Grid-based main layout with expanding output; ~44px control heights; per-mode hint lines using `MAX_*` from `crypto_core`; entropy bar caption; Enter / Ctrl+Enter / ⌘+Return bindings; copy-empty status; exported `MAX_ALPHANUMERIC_LENGTH` / `MAX_HEX_BYTES`; README + AGENT UX sections.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `src/crypto_core.py`, `src/strings.py`, `src/ui.py`, `tests/test_crypto.py`
- **Verification:** `.venv/bin/python -m pytest tests/ -v` → 19 passed; `python -m compileall -q src tests`; `PYTHONPATH=src python -c "import ui"`
- **Follow-ups:** Optional narrow-window layout (stack entropy controls); high-contrast theme toggle.

## Raouf: 2026-04-07 — Audit: i18n, limits, tests
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Full pass on `EntropyForge` (security, i18n, tests, docs)
- **Summary:** Moved remaining UI literals (`common.em_dash`, defaults) into `strings.py`; added max password length (4096) and hex bytes (512) in `crypto_core`; tests for limits, lone-sign parse, entropy edge case, and string-key coverage; README note on caps.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `src/crypto_core.py`, `src/strings.py`, `src/ui.py`, `tests/test_crypto.py`
- **Verification:** `.venv/bin/python -m pytest tests/ -v` → 19 passed; `python -m compileall -q src tests`
- **Follow-ups:** Optional `ruff`/`mypy`; segmented-button internal IDs if duplicate translated labels ever become possible.

## Raouf: 2026-04-07 — EntropyForge initial scaffold
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Portfolio-grade CSPRNG desktop app (`EntropyForge/`)
- **Summary:** Added `crypto_core` (stdlib `secrets` only), CustomTkinter `ui`, string keys in `strings.py`, `pytest` suite, `requirements.txt`, `.gitignore`, `README.md`, `git init` on `main`, and project `AGENT.md`.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `.gitignore`, `requirements.txt`, `src/__init__.py`, `src/main.py`, `src/ui.py`, `src/crypto_core.py`, `src/strings.py`, `tests/__init__.py`, `tests/test_crypto.py`
- **Verification:** `.venv/bin/python -m pytest tests/ -v` → 14 passed
- **Follow-ups:** Optional PyInstaller CI; add `pre-commit` or `ruff` if the repo grows.

## Raouf: template
- **Date:** (Australia/Sydney)
- **Scope:**
- **Summary:**
- **Files changed:**
- **Verification:**
- **Follow-ups:**
