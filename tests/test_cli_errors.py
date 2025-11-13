from pathlib import Path
import sys

from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from envsentry.cli import scan


def test_scan_reports_missing_file(tmp_path):
    runner = CliRunner()
    missing_file = tmp_path / ".env.missing"

    result = runner.invoke(scan, [str(missing_file)])

    assert result.exit_code != 0
    assert "No secrets detected" not in result.output
    assert "Failed to read" in result.output
