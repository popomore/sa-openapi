"""SQL CLI command (top-level alias for model sql)."""

from typing import TYPE_CHECKING

import click

from .output import print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.command("sql")
@click.argument("sql")
@click.option("--limit", type=int, default=100, help="Result limit")
@click.option(
    "--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table"
)
@click.pass_context
def sql(ctx, sql, limit, output_format):
    """Execute custom SQL query (alias for 'model sql')."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.model.sql_query(sql, limit=limit)

        data = result.data or []
        first_row = data[0] if data else []
        columns = result.columns or [f"col_{i}" for i in range(len(first_row))]

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
