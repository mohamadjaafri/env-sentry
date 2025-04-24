import click
from rich.console import Console
from envsentry.scanner import scan_env_file

console = Console()

@click.command()
@click.argument('filepath', default='.env')
def scan(filepath):
    """Scan .env file for potential secrets."""
    console.print(f"\n🔍 Scanning [bold]{filepath}[/bold]...\n")
    findings = scan_env_file(filepath)

    if not findings:
        console.print("✅ No secrets detected.\n", style="green")
    else:
        for line, key, value in findings:
            console.print(f"⚠️  Line {line}: {key} looks like a secret", style="bold yellow")

if __name__ == '__main__':
    scan()
