# API reference

EntropyForge is primarily a GUI application; the public Python surface is small
and stable for testing and scripting.

## Package

`entropyforge` — install with `pip install -e .` from the repository root.

### `entropyforge.crypto_core`

| Symbol | Description |
|--------|-------------|
| `MAX_ALPHANUMERIC_LENGTH` | Upper bound on password character count. |
| `MAX_HEX_BYTES` | Upper bound on hex key size in bytes. |
| `CryptoCoreError` | Carries `message_key` for locale lookup. |
| `parse_strict_int(raw)` | Strict decimal integer from user text. |
| `parse_positive_int(raw, error_key=...)` | Positive integer or `CryptoCoreError`. |
| `generate_alphanumeric(length)` | `secrets.choice` from 62-char alphabet. |
| `generate_hex_key(num_bytes)` | `secrets.token_hex`. |
| `generate_secure_int_inclusive(lo, hi)` | Uniform int via `secrets.randbelow`. |
| `entropy_bits_*` | Informational entropy estimates for the UI. |
| `paranoid_*` | Helpers for “large output” confirmation thresholds. |

### `entropyforge.i18n`

| Symbol | Description |
|--------|-------------|
| `load_locale(locale)` | Load `en` + overlay; sets RTL state. |
| `t(key)` | Resolve translated string. |
| `is_rtl()` | True for RTL locales (e.g. `ar`). |
| `current_locale()` | Active locale code. |

### `entropyforge.config`

| Symbol | Description |
|--------|-------------|
| `config_directory()` | `Path` to config dir (created if needed). |
| `load_settings()` / `save_settings(dict)` | JSON persistence. |

### `entropyforge.main`

| Symbol | Description |
|--------|-------------|
| `main()` | Configure logging, locale, launch `run_app`. |

### `entropyforge.ui`

| Symbol | Description |
|--------|-------------|
| `run_app(settings)` | Start CustomTkinter main loop (blocking). |

For scripting without GUI, prefer importing `crypto_core` only (see
`examples/`).
