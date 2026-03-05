"""Model CLI commands."""

import json
import re
from typing import TYPE_CHECKING

import click

from .output import console, print_error, print_json, print_table


def _camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _normalize_params(params: dict) -> dict:
    """Accept both camelCase and snake_case JSON keys."""
    return {_camel_to_snake(k): v for k, v in params.items()}

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def model():
    """Model commands (funnel, retention, attribution)."""
    pass


@model.command("funnel-report")
@click.option("--json", "json_str", required=True, help="Funnel parameters as JSON")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def funnel_report(ctx, json_str, output_format):
    """Get funnel analysis report."""
    try:
        params = _normalize_params(json.loads(json_str))
        client: SensorsAnalyticsClient = ctx.obj["client"]

        report = client.model.funnel_report(**params)

        if output_format == "json":
            print_json(report.model_dump(by_alias=True))
        else:
            # Convert steps to table
            data = [s.model_dump(by_alias=True) for s in report.steps]
            print_table(data, title="Funnel Report")
            console.print(f"\n[bold]Total:[/bold] {report.total}")
            console.print(f"[bold]Overall Conversion:[/bold] {report.overall_conversion:.2f}%")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@model.command("retention-report")
@click.option("--json", "json_str", required=True, help="Retention parameters as JSON")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def retention_report(ctx, json_str, output_format):
    """Get retention analysis report."""
    try:
        params = _normalize_params(json.loads(json_str))
        client: SensorsAnalyticsClient = ctx.obj["client"]

        report = client.model.retention_report(**params)

        if output_format == "json":
            print_json(report.model_dump(by_alias=True))
        else:
            data = [r.model_dump(by_alias=True) for r in report.data]
            print_table(data, title="Retention Report")
            console.print(f"\n[bold]Cohort Size:[/bold] {report.cohort_size}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@model.command("attribution-report")
@click.option("--json", "json_str", required=True, help="Attribution parameters as JSON")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def attribution_report(ctx, json_str, output_format):
    """Get attribution analysis report."""
    try:
        params = _normalize_params(json.loads(json_str))
        client: SensorsAnalyticsClient = ctx.obj["client"]

        report = client.model.attribution_report(**params)

        if output_format == "json":
            print_json(report.model_dump(by_alias=True))
        else:
            data = [a.model_dump(by_alias=True) for a in report.data]
            print_table(data, title="Attribution Report")
            console.print(f"\n[bold]Total Conversions:[/bold] {report.total_conversions}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@model.command("sql")
@click.option("--sql", required=True, help="SQL query")
@click.option("--limit", type=int, default=100, help="Result limit")
@click.option(
    "--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table"
)
@click.pass_context
def sql(ctx, sql, limit, output_format):
    """Execute custom SQL query."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.model.sql_query(sql, limit=limit)

        rows = []
        columns = result.get("columns", [])
        for row in result.get("rows", []):
            rows.append(dict(zip(columns, row, strict=False)))

        if output_format == "json":
            print_json(rows)
        elif output_format == "csv":
            from .output import print_csv

            print_csv(rows)
        else:
            print_table(rows, title="SQL Query Results")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@model.command("explain-sql")
@click.argument("sql")
@click.pass_context
def explain_sql(ctx, sql):
    """Get SQL execution plan. (Not available in Model v1 API)"""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.model.explain_sql(sql)
        print_json(result.model_dump(by_alias=True))
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@model.command("validate-sql")
@click.argument("sql")
@click.pass_context
def validate_sql(ctx, sql):
    """Validate SQL syntax. (Not available in Model v1 API)"""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.model.validate_sql(sql)
        if result.valid:
            console.print("[green]✓[/green] SQL is valid")
        else:
            console.print(f"[red]✗[/red] {result.error}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
