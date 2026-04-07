# Packaging, distribution, and code signing

This document is **informational**. EntropyForge does not perform notarization or Windows signing in this repository.

## PyInstaller

- **One-file:** see `entropyforge.spec` in the project root (windowed executable, single file).
- **One-folder:** see `entropyforge_onedir.spec` (folder bundle with `COLLECT`, faster startup than one-file on some systems).

Typical workflow (after `pip install -e .` and `pip install pyinstaller`):

```bash
pyinstaller entropyforge.spec
# or
pyinstaller entropyforge_onedir.spec
```

Adjust `--add-data` / `datas=` separators for Windows (`;`) vs Linux/macOS (`:`) if you build on another OS.

## macOS notarization (manual)

Apple requires notarization for distribution outside the Mac App Store when Gatekeeper is enabled. High-level steps:

1. Enroll in the Apple Developer Program and create signing certificates (Developer ID Application).
2. Sign the app bundle or binary with `codesign` (often with `--options runtime` for hardened runtime).
3. Submit the signed product for notarization with `notarytool` or `altool` using an app-specific password or API key.
4. Staple the ticket to the app: `xcrun stapler staple ...`.

Verify against Apple’s current documentation; process and tools change with Xcode and macOS versions.

## Windows SmartScreen / code signing (manual)

Unsigned executables often trigger SmartScreen warnings. Commercial or organizational code signing uses:

1. A code signing certificate from a trusted CA (often EV for immediate reputation).
2. Sign the `.exe` with `signtool` (Windows SDK) and timestamp the signature.

Consult Microsoft’s latest guidance on Authenticode and SmartScreen reputation.

## CI artifacts

The GitHub Actions workflow builds a **one-folder** PyInstaller bundle on Ubuntu and uploads it as an artifact. That binary targets **Linux**; it is not a macOS `.app` or Windows `.exe`. Use matching runners (e.g. `macos-latest`, `windows-latest`) if you need platform-specific installers.
