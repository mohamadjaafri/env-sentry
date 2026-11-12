from click.testing import CliRunner

from envsentry.cli import scan


def test_scan_reports_missing_file_with_operational_exit_code(tmp_path):
    runner = CliRunner()
    missing_file = tmp_path / ".env.missing"

    result = runner.invoke(scan, [str(missing_file)])

    assert result.exit_code == 2
    assert "No secrets detected" not in result.output
    assert "Failed to read" in result.output
