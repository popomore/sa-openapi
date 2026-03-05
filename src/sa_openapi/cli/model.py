"""Model CLI commands."""

import json
import re
from typing import TYPE_CHECKING

import click

from .output import console, print_error, print_json, print_table


def _camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _normalize_params(value):
    """Accept both camelCase and snake_case JSON keys recursively."""
    if isinstance(value, dict):
        return {_camel_to_snake(k): _normalize_params(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_params(v) for v in value]
    return value

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
            if hasattr(report, "model_dump"):
                print_json(report.model_dump(by_alias=True))
            else:
                print_json(report)
        else:
            if hasattr(report, "steps"):
                data = [s.model_dump(by_alias=True) for s in report.steps]
                print_table(data, title="Funnel Report")
                console.print(f"\n[bold]Total:[/bold] {report.total}")
                console.print(f"[bold]Overall Conversion:[/bold] {report.overall_conversion:.2f}%")
            else:
                rows = report.get("detail_rows") or report.get("rows") or []
                cols = report.get("metadata_columns") or report.get("columns") or []
                if cols and rows and isinstance(rows[0], (list, tuple)):
                    table_rows = [dict(zip(cols, r, strict=False)) for r in rows]
                else:
                    table_rows = rows if isinstance(rows, list) else [rows]
                print_table(table_rows, title="Funnel Report")
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
            if hasattr(report, "model_dump"):
                print_json(report.model_dump(by_alias=True))
            else:
                print_json(report)
        else:
            if hasattr(report, "data"):
                data = [r.model_dump(by_alias=True) for r in report.data]
                print_table(data, title="Retention Report")
                console.print(f"\n[bold]Cohort Size:[/bold] {report.cohort_size}")
            else:
                rows = report.get("detail_rows") or report.get("rows") or []
                cols = report.get("metadata_columns") or report.get("columns") or []
                table_rows = [dict(zip(cols, r, strict=False)) for r in rows] if cols and rows else rows
                print_table(table_rows, title="Retention Report")
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
            if hasattr(report, "model_dump"):
                print_json(report.model_dump(by_alias=True))
            else:
                print_json(report)
        else:
            if hasattr(report, "data"):
                data = [a.model_dump(by_alias=True) for a in report.data]
                print_table(data, title="Attribution Report")
                console.print(f"\n[bold]Total Conversions:[/bold] {report.total_conversions}")
            else:
                rows = report.get("detail_rows") or report.get("rows") or []
                cols = report.get("metadata_columns") or report.get("columns") or []
                table_rows = [dict(zip(cols, r, strict=False)) for r in rows] if cols and rows else rows
                print_table(table_rows, title="Attribution Report")
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
    print_error("`explain-sql` is not supported by Model v1 API.")
    raise click.Abort()


@model.command("validate-sql")
@click.argument("sql")
@click.pass_context
def validate_sql(ctx, sql):
    """Validate SQL syntax. (Not available in Model v1 API)"""
    print_error("`validate-sql` is not supported by Model v1 API.")
    raise click.Abort()
