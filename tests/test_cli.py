import json

from click.testing import CliRunner

from envsentry.cli import scan


def test_scan_reports_missing_file_with_operational_exit_code(tmp_path):
    runner = CliRunner()
    result = runner.invoke(scan, [str(tmp_path / ".env.missing")])

    assert result.exit_code == 2
    assert "Failed to read" in result.output


def test_scan_returns_nonzero_when_findings_exist(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("SERVICE_TOKEN=fake-example-token\n", encoding="utf-8")

    result = CliRunner().invoke(scan, [str(env_file)])

    assert result.exit_code == 1
    assert "SERVICE_TOKEN" in result.output
    assert "fake-example-token" not in result.output


def test_json_output_is_machine_readable_and_redacted(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("SERVICE_TOKEN=fake-example-token\n", encoding="utf-8")

    result = CliRunner().invoke(scan, ["--json", str(env_file)])

    payload = json.loads(result.output)
    assert result.exit_code == 1
    assert payload["files_scanned"] == 1
    assert payload["findings"][0]["key"] == "SERVICE_TOKEN"
    assert "fake-example-token" not in result.output


def test_no_findings_returns_zero(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("APP_ENV=production\n", encoding="utf-8")

    result = CliRunner().invoke(scan, [str(env_file)])

    assert result.exit_code == 0
    assert "No potential secrets" in result.output


def test_can_report_without_failing_pipeline(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("SERVICE_TOKEN=fake-example-token\n", encoding="utf-8")

    result = CliRunner().invoke(scan, ["--no-fail-on-findings", str(env_file)])

    assert result.exit_code == 0
