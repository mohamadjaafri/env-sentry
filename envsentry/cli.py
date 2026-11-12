"""Command-line interface for env-sentry."""

from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from envsentry.scanner import scan_env_file

console = Console()


@click.command()
@click.argument(
    "filepaths",
    nargs=-1,
    type=click.Path(path_type=Path, dir_okay=False),
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Print machine-readable JSON instead of terminal output.",
)
@click.option(
    "--fail-on-findings/--no-fail-on-findings",
    default=True,
    show_default=True,
    help="Return exit code 1 when a finding is detected.",
)
@click.version_option()
def scan(filepaths: tuple[Path, ...], json_output: bool, fail_on_findings: bool) -> None:
    """Scan one or more dotenv files for possible secrets.

    When no FILEPATH is supplied, env-sentry scans .env in the current directory.
    Finding output is always redacted. Values are never printed or serialized.
    """
    targets = filepaths or (Path(".env"),)
    findings = []
    errors = []

    for path in targets:
        try:
            findings.extend(scan_env_file(path))
        except (OSError, UnicodeError) as exc:
            errors.append({"file": str(path), "error": str(exc)})

    if json_output:
        click.echo(
            json.dumps(
                {
                    "files_scanned": len(targets) - len(errors),
                    "findings": [finding.to_dict() for finding in findings],
                    "errors": errors,
                },
                indent=2,
            )
        )
    else:
        for error in errors:
            console.print(
                f"[bold red]Failed to read {error['file']}:[/bold red] {error['error']}"
            )

        if findings:
            table = Table(title="Potential secrets detected")
            table.add_column("File")
            table.add_column("Line", justify="right")
            table.add_column("Key")
            table.add_column("Reason")
            for finding in findings:
                table.add_row(
                    finding.file,
                    str(finding.line),
                    finding.key,
                    finding.reason,
                )
            console.print(table)
        elif not errors:
            console.print("[green]No potential secrets detected.[/green]")

    if errors:
        raise click.exceptions.Exit(2)
    if findings and fail_on_findings:
        raise click.exceptions.Exit(1)


if __name__ == "__main__":
    scan()
