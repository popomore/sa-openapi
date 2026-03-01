"""Output formatting for CLI."""

from typing import Any

from rich.console import Console
from rich.table import Table


console = Console()


def print_table(data: list[dict[str, Any]], title: str | None = None) -> None:
    """Print data as a table."""
    if not data:
        console.print("[dim]No data[/dim]")
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")

    # Add columns
    for key in data[0].keys():
        table.add_column(key.replace("_", " ").title())

    # Add rows
    for row in data:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


def print_json(data: Any) -> None:
    """Print data as JSON."""
    import json

    console.print_json(json.dumps(data, indent=2, ensure_ascii=False))


def print_csv(data: list[dict[str, Any]]) -> None:
    """Print data as CSV."""
    import csv
    import io

    if not data:
        return

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    console.print(output.getvalue())


def print_list(items: list[str], title: str | None = None) -> None:
    """Print data as a list."""
    if title:
        console.print(f"\n[bold]{title}[/bold]")

    for item in items:
        console.print(f"  • {item}")


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]⚠[/yellow] {message}")
