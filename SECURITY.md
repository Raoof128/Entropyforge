# Security policy

EntropyForge is a small personal project maintained by one person. It has not had an independent security review; the README lists its limits.

## Supported versions

Only the current `main` branch is maintained.

## Reporting a vulnerability

**Please do not** open a public issue for a security problem. Use GitHub's private vulnerability reporting: the **Report a vulnerability** button on this repository's *Security* tab, or <https://github.com/Raoof128/Entropyforge/security/advisories/new>.

Useful things to include: what the problem is and its impact, steps to reproduce, and a suggested fix if you have one. Reports are read as time allows; there is no guaranteed response time.

## Scope

**In scope**

- Misuse of randomness or predictable output in `entropyforge.crypto_core`
- Secrets reaching the log file, or handled unsafely in the clipboard flow
- Input validation bugs that crash or hang the desktop app

**Out of scope (examples)**

- Physical access to an unlocked machine running the app
- Threat models that assume a compromised OS or kernel
- Limits the README already states (values cannot be wiped from memory; clipboard managers keep their own copies)
- Third-party dependencies (report upstream)

## Design assumptions

EntropyForge uses Python's `secrets` module (the operating system's CSPRNG). It does **not** use `random` for generation. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
