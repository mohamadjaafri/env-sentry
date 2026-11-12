# env-sentry

**env-sentry** is a small DevSecOps utility that scans dotenv files for likely secrets before they enter source control.

It is designed as a local developer check and a CI pipeline gate. The scanner reports the file, line, variable name, and detection reason. **It never prints, stores, or serializes the detected value.**

## Why this exists

Credentials often enter repositories through local configuration files. env-sentry adds a lightweight control before commit and in CI. It is intentionally heuristic: it catches suspicious variable names and common high-entropy value shapes without claiming to replace a dedicated secret-scanning platform.

## Capabilities

- Scan one or multiple dotenv files.
- Detect sensitive-looking keys such as `API_TOKEN`, `DB_PASSWORD`, and `PRIVATE_KEY`.
- Flag long base64-like and hexadecimal values.
- Support `export KEY=value`, quoted values, comments, and blank lines.
- Emit human-readable terminal output or machine-readable JSON.
- Return explicit exit codes for findings and file errors.
- Integrate with pre-commit and GitHub Actions.
- Keep finding records redacted. Secret values are not part of the result model.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
env-sentry .env
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Scan several files:

```bash
env-sentry .env .env.local config/.env.staging
```

Machine-readable output:

```bash
env-sentry --json .env
```

## Exit codes

| Code | Meaning |
|---|---|
| `0` | No findings, or findings reported with `--no-fail-on-findings` |
| `1` | One or more potential secrets detected |
| `2` | One or more files could not be read |

These semantics make the command suitable for local hooks and CI pipeline gates.

## Example

Given a file containing:

```dotenv
APP_ENV=production
API_TOKEN=fake-example-value
```

env-sentry reports the variable name and line number. It does not output the value.

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest --cov=envsentry --cov-report=term-missing
```

## Architecture

```text
CLI (Click)
   |
   +-- accepts one or more dotenv paths
   |
Scanner
   |
   +-- parses dotenv-style assignments
   +-- applies key-name and value-shape heuristics
   +-- creates redacted Finding objects
   |
Output
   +-- Rich terminal table
   +-- JSON for CI and automation
   |
Exit status
   +-- 0: clean / non-blocking report
   +-- 1: findings
   +-- 2: read error
```

## Security model and limitations

- This tool performs static, heuristic checks. It does not validate whether a credential is active.
- It does not replace GitHub secret scanning, Gitleaks, TruffleHog, or a centralized secrets-management platform.
- It does not execute shell expressions or resolve variable references.
- Heuristics can produce false positives and can miss secrets with unusual formats.
- Never commit real credentials, even when a local scan reports no findings.
- Findings contain metadata only. The scanner deliberately does not retain the original value.

See [SECURITY.md](SECURITY.md) for responsible disclosure guidance.

## Roadmap

- Add configurable detection rules and allowlists.
- Add support for structured secret-scan output formats.
- Add optional integration tests for pre-commit behavior.
- Evaluate entropy-based detection with a false-positive test corpus.

## License

MIT
