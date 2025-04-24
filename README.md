# env-sentry

**env-sentry** is a CLI tool that scans `.env` files for hardcoded secrets before you push them to a repository.

---

## 🔍 Features

- Detects suspicious keys like `SECRET`, `TOKEN`, `KEY`, `PASSWORD`, `CLIENT_SECRET`
- Flags potentially sensitive values (e.g. base64 strings, long hex values)
- Styled terminal output using `rich`
- Simple CLI usage with `click`

---

## 🛠️ Installation

```bash
git clone https://github.com/mohamadjaafri/env-sentry.git
cd env-sentry
pip install -e .
```

---

## 🚀 Usage

```bash
env-sentry .env
```

Example output:

```
🔍 Scanning .env...

⚠️  Line 2: JWT_SECRET looks like a secret
⚠️  Line 5: API_KEY is 64 chars long – potential sensitive value
✅  No secrets detected in .env.dev
```

---

## 📦 Project Structure

```
env-sentry/
├── envsentry/
│   ├── cli.py
│   └── scanner.py
├── setup.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Optional: Git Hook Integration

You can use [pre-commit](https://pre-commit.com/) to run `env-sentry` before each commit.

**.pre-commit-config.yaml** example:

```yaml
repos:
  - repo: local
    hooks:
      - id: env-sentry
        name: env-sentry check
        entry: env-sentry .env
        language: system
        files: \.env$
```

Then activate it:

```bash
pre-commit install
```

---

## 📄 License

MIT License
