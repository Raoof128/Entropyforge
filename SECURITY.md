# Security policy

## Supported versions

Security fixes are applied to the latest release line on the default branch
(`main`). Older tags may not receive backports unless agreed with maintainers.

## Reporting a vulnerability

**Please do not** open a public issue for security vulnerabilities.

Instead, report privately:

1. Use **GitHub Security Advisories** for this repository (*Security* tab →
   *Report a vulnerability*), if enabled; or
2. Email maintainers with a clear subject line (e.g. `[SECURITY] EntropyForge`)
   and include:
   - Description of the issue and impact
   - Steps to reproduce (proof-of-concept if safe)
   - Suggested fix (optional)

You should receive an acknowledgment within a few business days. Critical
issues will be prioritized.

## Scope

**In scope**

- Misuse of randomness or predictable output in `entropyforge.crypto_core`
- Unsafe handling of secrets in memory, logging, or clipboard flows
- Input validation bugs that allow crashes or denial of service in the desktop
  app

**Out of scope (examples)**

- Physical access to an unlocked machine running the app
- Threat models that assume a compromised OS or kernel
- Third-party dependencies (report upstream per their policies; we may bump
  versions here)

## Design assumptions

EntropyForge uses Python’s `secrets` module (OS-provided CSPRNG). It does **not**
use `random` for cryptographic generation. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Safe harbor

We support good-faith security research. Do not access data you do not own, and
do not perform destructive testing against production systems without permission.
