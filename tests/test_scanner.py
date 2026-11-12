from envsentry.scanner import scan_env_file


def test_detects_sensitive_key_without_retaining_value(tmp_path):
    env_file = tmp_path / ".env"
    secret = "this-is-a-fake-example-token"
    env_file.write_text(f"API_TOKEN={secret}\n", encoding="utf-8")

    findings = scan_env_file(env_file)

    assert len(findings) == 1
    assert findings[0].key == "API_TOKEN"
    assert "sensitive-looking variable name" in findings[0].reason
    assert secret not in repr(findings[0])
    assert not hasattr(findings[0], "value")


def test_detects_long_hex_value(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(f"CACHE_ID={'a' * 40}\n", encoding="utf-8")

    findings = scan_env_file(env_file)

    assert len(findings) == 1
    assert "hexadecimal" in findings[0].reason


def test_ignores_comments_blank_lines_and_placeholders(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# API_SECRET=not-a-real-secret\n\n"
        "export APP_ENV=production\n"
        "API_SECRET=changeme\n"
        "OPTIONAL=\n",
        encoding="utf-8",
    )

    assert scan_env_file(env_file) == []


def test_supports_quoted_values_and_inline_comments(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        'DB_PASSWORD="fake-password"\n'
        "APP_MODE=production # regular comment\n",
        encoding="utf-8",
    )

    findings = scan_env_file(env_file)

    assert len(findings) == 1
    assert findings[0].key == "DB_PASSWORD"
    assert findings[0].line == 1
