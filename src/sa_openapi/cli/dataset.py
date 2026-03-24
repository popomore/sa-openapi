"""Dataset CLI commands."""

import json
from typing import TYPE_CHECKING

import click

from .output import console, print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def dataset():
    """Dataset commands."""
    pass


@dataset.command("detail")
@click.argument("dataset_id", type=int)
@click.option("--model-type", help="Model type filter")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_dataset_detail(ctx, dataset_id, model_type, output_format):
    """Get dataset detail information."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        ds = client.dataset.get_dataset_detail(dataset_id, model_type=model_type)

        if output_format == "json":
            print_json(ds.model_dump(by_alias=True))
        else:
            data = {
                "dataset_id": ds.dataset_id,
                "dataset_cname": ds.dataset_cname,
                "dataset_type": ds.dataset_type,
                "sync_status": ds.sync_status,
                "scheduler_status": ds.scheduler_status,
                "columns_count": len(ds.columns or []),
            }
            print_table([data], title=f"Dataset {dataset_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dataset.command("list")
@click.option("--group-name", help="Filter by group name")
@click.option("--page-index", type=int, default=1, help="Page index")
@click.option("--page-size", type=int, default=20, help="Page size")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_datasets(ctx, group_name, page_index, page_size, output_format):
    """List all datasets."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        params: dict = {"page_index": page_index, "page_size": page_size}
        if group_name:
            params["group_name"] = group_name

        datasets = client.dataset.list_datasets(params)

        if output_format == "json":
            print_json([d.model_dump(by_alias=True) for d in datasets])
        else:
            data = [
                {
                    "dataset_id": d.dataset_id,
                    "dataset_cname": d.dataset_cname,
                    "dataset_type": d.dataset_type,
                    "is_scheduler_pause": d.is_scheduler_pause,
                }
                for d in datasets
            ]
            print_table(data, title=f"Datasets ({len(data)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dataset.command("groups")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_groups(ctx, output_format):
    """List dataset groups."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        groups = client.dataset.list_dataset_groups()

        if output_format == "json":
            print_json([g.model_dump(by_alias=True) for g in groups])
        else:
            data = [{"id": g.id, "group_name": g.group_name} for g in groups]
            print_table(data, title=f"Dataset Groups ({len(data)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dataset.command("sql")
@click.argument("sql")
@click.option("--description", help="Query description")
@click.option(
    "--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table"
)
@click.pass_context
def sql_query(ctx, sql, description, output_format):
    """Execute SQL query on dataset."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.dataset.sql_query(sql, description=description)

        columns = result.columns or []
        rows_raw = result.data or []
        rows = [dict(zip(columns, row, strict=False)) for row in rows_raw]

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


@dataset.command("model-query")
@click.option("--dataset-id", required=True, type=int, help="Dataset ID")
@click.option("--json", "json_str", required=True, help="Query parameters as JSON")
@click.option(
    "--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table"
)
@click.pass_context
def model_query(ctx, dataset_id, json_str, output_format):
    """Query dataset by dimension/measure rules.

    Example JSON: '{"dimensions": ["city"], "measures": [{"column_name": "pv", "aggregation": "SUM"}]}'
    """
    try:
        try:
            params = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise click.BadParameter(f"--json must be valid JSON: {e}") from e
        if not isinstance(params, dict):
            raise click.BadParameter("--json must decode to a JSON object")
        params["dataset_id"] = dataset_id
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.dataset.model_query(params)

        columns = result.columns or []
        rows_raw = result.data or []
        rows = [dict(zip(columns, row, strict=False)) for row in rows_raw]

        if output_format == "json":
            print_json(result.model_dump(by_alias=True))
        elif output_format == "csv":
            from .output import print_csv

            print_csv(rows)
        else:
            print_table(rows, title="Model Query Results")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dataset.command("refresh")
@click.argument("dataset_id", type=int)
@click.option("--sync-type", help="Sync type")
@click.option("--from-date", help="Refresh from date (YYYY-MM-DD)")
@click.option("--to-date", help="Refresh to date (YYYY-MM-DD)")
@click.pass_context
def refresh_dataset(ctx, dataset_id, sync_type, from_date, to_date):
    """Trigger dataset data refresh."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.dataset.refresh_dataset(
            dataset_id,
            sync_type=sync_type,
            refresh_from_date=from_date,
            refresh_to_date=to_date,
        )
        console.print(f"[green]Refresh triggered. Sync task ID: {result.sync_task_id}[/green]")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dataset.command("sync-status")
@click.argument("sync_task_id")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def sync_task_detail(ctx, sync_task_id, output_format):
    """Get sync task status.

    SYNC_TASK_ID: Task ID returned by the refresh command
    """
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.dataset.get_sync_task_detail(sync_task_id)

        if output_format == "json":
            print_json(result.model_dump(by_alias=True))
        else:
            data = {
                "sync_task_id": result.sync_task_id,
                "sync_status": result.sync_status,
                "start_time": result.start_time,
                "end_time": result.end_time,
                "duration_seconds": result.duration_seconds,
                "failed_reason": result.failed_reason,
            }
            print_table([data], title=f"Sync Task {sync_task_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
