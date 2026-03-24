"""Model CLI commands."""

import json
import re
from typing import TYPE_CHECKING, Any

import click

from .output import console, print_error, print_json, print_table


def _camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"_", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"_", s1).lower()


def _normalize_params(value):
    """Accept both camelCase and snake_case JSON keys recursively."""
    if isinstance(value, dict):
        return {_camel_to_snake(k): _normalize_params(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_normalize_params(v) for v in value]
    return value


if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def model():
    """Model commands (funnel, retention, attribution)."""
    pass


def _display_v1_report(report: Any, title: str) -> None:
    """Display v1 report with metadata_columns and detail_rows."""
    # Get metadata columns and detail rows
    metadata = getattr(report, "metadata_columns", None) or {}
    detail_rows = getattr(report, "detail_rows", None) or []
    truncated = getattr(report, "truncated", False)

    # Convert metadata_columns dict to column names
    columns = list(metadata.keys()) if metadata else []

    # If no metadata, try to get columns from first row
    if not columns and detail_rows:
        # detail_rows is list of lists, infer column count
        first_row = detail[0] if (detail := detail_rows) and detail else []
        columns = [f"col_{i}" for i in range(len(first_row))]

    # Build table rows
    table_rows = []
    for row in detail_rows:
        if isinstance(row, list | tuple):
            table_rows.append(dict(zip(columns, row, strict=False)))
        else:
            table_rows.append(row)

    if table_rows:
        print_table(table_rows, title=title)
    else:
        console.print("[yellow]No data returned[/yellow]")

    if truncated:
        console.print("[yellow]Warning: Results were truncated[/yellow]")


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
            _display_v1_report(report, "Funnel Report")
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
            _display_v1_report(report, "Retention Report")
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
            _display_v1_report(report, "Attribution Report")
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

        columns = result.columns or []
        data = result.data or []

        if output_format == "json":
            print_json(result.model_dump(by_alias=True))
        elif output_format == "csv":
            from .output import print_csv

            rows = [dict(zip(columns, row, strict=False)) for row in data]
            print_csv(rows)
        else:
            rows = [dict(zip(columns, row, strict=False)) for row in data]
            print_table(rows, title="SQL Query Results")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@model.command("explain-sql")
@click.argument("sql")
@click.pass_context
def explain_sql(ctx, sql):
    """Get SQL execution plan. (Not available in Model v1 API)"""
    print_error(" is not supported by Model v1 API.")
    raise click.Abort()


@model.command("validate-sql")
@click.argument("sql")
@click.pass_context
def validate_sql(ctx, sql):
    """Validate SQL syntax. (Not available in Model v1 API)"""
    print_error(" is not supported by Model v1 API.")
    raise click.Abort()
