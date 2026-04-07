# EntropyForge — Agent Rules

## Scope
- Python package `entropyforge` under `src/`: CustomTkinter UI + stdlib-only crypto (`secrets`).
- User-visible strings live in `entropyforge/locales/*.json` (loaded by `i18n.py`); never hardcode UI copy in Python.
- Generation logic in `crypto_core.py`; UI in `ui.py`; settings in `config.py` (JSON via `platformdirs`).

## UI / UX
- Prefer grid with expanding rows for the output region; set a sensible `minsize` so mode labels do not collapse unreadably.
- Primary controls (mode radios, generate, copy) target ~44px minimum height; document shortcuts in locales (`hint.shortcuts`).
- Surface limits and rules beside inputs via `hint.*` keys; never hardcode user-visible copy in `ui.py`.
- Explain the entropy bar in plain language (`entropy.hint_bar`); status line feedback for copy (including empty clipboard attempts).
- RTL locales (`ar`, `he`, `fa`, `ur` via `i18n.is_rtl()`): mirror horizontal pack/grid order, swap output header columns, entropy row, and primary button order; restart after locale change to rebuild chrome.

## Quality
- No `random` module for security-sensitive generation.
- Validate and sanitize numeric inputs; fail with clear, keyed error messages; reject non-ASCII digit strings that `isdigit()` would accept.
- Add or update tests when changing `crypto_core` behavior.
- Cap password length and hex byte size in `crypto_core` to limit allocation DoS; every `CryptoCoreError.message_key` must exist in `locales/en.json` (and overlays).

## Tooling
- `ruff check src tests`; `pytest` after substantive edits; `pip install -e ".[dev]"` for local dev.

---

## Raouf: 2026-04-07 — EntropyForge initial scaffold
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Portfolio-grade CSPRNG desktop app (`EntropyForge/`)
- **Summary:** Added `crypto_core` (stdlib `secrets` only), CustomTkinter `ui`, string keys in `strings.py`, `pytest` suite, `requirements.txt`, `.gitignore`, `README.md`, `git init` on `main`, and project `AGENT.md`.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `.gitignore`, `requirements.txt`, `src/__init__.py`, `src/main.py`, `src/ui.py`, `src/crypto_core.py`, `src/strings.py`, `tests/__init__.py`, `tests/test_crypto.py`
- **Verification:** `.venv/bin/python -m pytest tests/ -v` → 14 passed
- **Follow-ups:** Optional PyInstaller CI; add `pre-commit` or `ruff` if the repo grows.

---

## Raouf: 2026-04-07 — Audit: i18n, limits, tests
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Full pass on `EntropyForge` (security, i18n, tests, docs)
- **Summary:** Moved remaining UI literals (`common.em_dash`, defaults) into `strings.py`; added max password length (4096) and hex bytes (512) in `crypto_core`; tests for limits, lone-sign parse, entropy edge case, and string-key coverage; README note on caps.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `src/crypto_core.py`, `src/strings.py`, `src/ui.py`, `tests/test_crypto.py`
- **Verification:** `.venv/bin/python -m pytest tests/ -v` → 19 passed; `python -m compileall -q src tests`
- **Follow-ups:** Optional `ruff`/`mypy`; segmented-button internal IDs if duplicate translated labels ever become possible.

---

## Raouf: 2026-04-07 — Audit: UI/UX
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** EntropyForge interface and experience
- **Summary:** Grid-based main layout with expanding output; ~44px control heights; per-mode hint lines using `MAX_*` from `crypto_core`; entropy bar caption; Enter / Ctrl+Enter / ⌘+Return bindings; copy-empty status; exported `MAX_ALPHANUMERIC_LENGTH` / `MAX_HEX_BYTES`; README + AGENT UX sections.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `src/crypto_core.py`, `src/strings.py`, `src/ui.py`, `tests/test_crypto.py`
- **Verification:** `.venv/bin/python -m pytest tests/ -v` → 19 passed; `python -m compileall -q src tests`; `PYTHONPATH=src python -c "import ui"`
- **Follow-ups:** Optional narrow-window layout (stack entropy controls); high-contrast theme toggle.

---

## Raouf: 2026-04-07 — Feature pack: i18n, settings, CI, packaging
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** EntropyForge “add all” improvements (locales EN/AR, presets, output tools, paranoid dialogs, clipboard timer, first-run banner, logging, `pyproject.toml` + `entropyforge` console script, CI, ruff, hypothesis, PyInstaller spec, lockfile, strict ASCII integer parsing fix).
- **Files changed:** `pyproject.toml`, `requirements.txt`, `requirements-lock.txt`, `entropyforge.spec`, `.github/workflows/ci.yml`, `README.md`, `AGENT.md`, `CHANGELOG.md`, `.gitignore`, `src/entropyforge/*` (new package), `tests/*`; removed flat `src/main.py`, `src/ui.py`, `src/crypto_core.py`, `src/strings.py`, `src/__init__.py`.
- **Verification:** `pip install -e ".[dev]"`; `pytest tests/ -v` (25 tests); `ruff check src tests`; `python -c` Arabic `load_locale('ar')`.
- **Follow-ups:** Optional one-dir PyInstaller bundle; stronger RTL layout for Arabic; automated locale coverage tests.

---

## Raouf: 2026-04-07 — Follow-ups: RTL, PyInstaller onedir, locale tests, packaging docs
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Optional follow-ups from prior roadmap
- **Summary:** RTL mirrored chrome for `i18n.is_rtl()` locales (`ar`, `he`, `fa`, `ur`); `entropyforge_onedir.spec` + CI job uploading Linux onedir artifact; AST test ensuring every literal `CryptoCoreError("…")` in `crypto_core.py` exists in `locales/en.json`; `docs/PACKAGING.md` for notarization/signing (documentation only); README/AGENT updates.
- **Files changed:** `AGENT.md`, `CHANGELOG.md`, `README.md`, `.github/workflows/ci.yml`, `docs/PACKAGING.md`, `entropyforge_onedir.spec`, `src/entropyforge/i18n.py`, `src/entropyforge/ui.py`, `tests/test_crypto_core_locale_keys.py`
- **Verification:** `pytest tests/ -v` → 27 passed; `ruff check src tests`
- **Follow-ups:** macOS/Windows PyInstaller builds on native runners if you ship desktop binaries.

---

## Raouf: 2026-04-07 — Production audit: docs, governance, tests, CI
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Industry-facing audit — coverage threshold, config/main/logging tests, README and CI alignment
- **Summary:** Added `tests/test_config.py`, `test_logging_config.py`, `test_main.py` (happy path + exception re-raise); `test_config_directory` exercises `platformdirs` wiring; CI runs `ruff format --check`, `ruff check`, and `pytest` with coverage; root `README.md` rewritten with TOC, doc links, community/security tables, quality gates, placeholder URL note; `docs/README.md` links to `examples/`; `Makefile` `check` already matches local workflow.
- **Files changed:** `README.md`, `.github/workflows/ci.yml`, `docs/README.md`, `tests/test_config.py`, `tests/test_logging_config.py`, `tests/test_main.py`, `AGENT.md`, `CHANGELOG.md`
- **Verification:** `ruff format --check src tests`; `ruff check src tests`; `pytest tests/ -v --cov=entropyforge` → 33 passed, total coverage ≥ 88% (`fail_under` in `pyproject.toml`).
- **Follow-ups:** Replace placeholder GitHub URLs in `pyproject.toml` when remote exists; optional codecov upload in CI.

---

## Raouf: 2026-04-07 — Remove Dependabot; publish to GitHub
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Repository hosting and dependency automation
- **Summary:** Removed `.github/dependabot.yml`; set `[project.urls]` to `https://github.com/Raoof128/entropyforge`; removed README placeholder URL note; added `.hypothesis/` to `.gitignore`; initial commit pushed to public `Raoof128/entropyforge`.
- **Files changed:** `.github/dependabot.yml` (removed), `.gitignore`, `pyproject.toml`, `README.md`, `AGENT.md`, `CHANGELOG.md`
- **Verification:** `gh repo create` + `git push` (see session); local `pytest` unchanged by these edits.
- **Follow-ups:** None required for hosting.

---

## Raouf: 2026-04-07 — Canonical GitHub URLs (Raoof128)
- **Date:** 2026-04-07 (Australia/Sydney)
- **Scope:** Package metadata
- **Summary:** `[project.urls]` now use `https://github.com/Raoof128/entropyforge` to match GitHub’s canonical username casing and the configured remote.
- **Files changed:** `pyproject.toml`, `AGENT.md`, `CHANGELOG.md`
- **Verification:** `git push origin main`
- **Follow-ups:** None
