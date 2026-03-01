"""Dataset CLI commands."""

import click

from ..client import SensorsAnalyticsClient
from .output import print_error, print_json, print_table


@click.group()
def dataset():
    """Dataset commands."""
    pass


@dataset.command("list")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_datasets(ctx, output_format):
    """List all datasets."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        datasets = client.dataset.list_dataset()

        data = [d.model_dump(by_alias=True) for d in datasets]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title="Datasets")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@dataset.command("get")
@click.argument("dataset_id", type=int)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_dataset(ctx, dataset_id, output_format):
    """Get dataset details."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        ds = client.dataset.get_dataset(dataset_id)

        data = ds.model_dump(by_alias=True)

        if output_format == "json":
            print_json(data)
        else:
            print_table([data], title=f"Dataset {dataset_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@dataset.command("schema")
@click.argument("dataset_id", type=int)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_schema(ctx, dataset_id, output_format):
    """Get dataset schema."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        schema = client.dataset.get_schema(dataset_id)

        data = [f.model_dump(by_alias=True) for f in schema.fields]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title=f"Dataset {dataset_id} Schema")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@dataset.command("sql-query")
@click.option("--dataset-id", required=True, type=int, help="Dataset ID")
@click.option("--sql", required=True, help="SQL query")
@click.option("--limit", type=int, default=100, help="Result limit")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table")
@click.pass_context
def sql_query(ctx, dataset_id, sql, limit, output_format):
    """Execute SQL query on dataset."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.dataset.sql_query(dataset_id, sql, limit=limit)

        rows = []
        for row in result.rows:
            rows.append(dict(zip(result.columns, row)))

        if output_format == "json":
            print_json(rows)
        elif output_format == "csv":
            from .output import print_csv
            print_csv(rows)
        else:
            print_table(rows, title=f"Dataset {dataset_id} Query Results")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@dataset.command("saved-queries")
@click.argument("dataset_id", type=int)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_saved_queries(ctx, dataset_id, output_format):
    """List saved queries for dataset."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        queries = client.dataset.list_saved_query(dataset_id)

        data = [q.model_dump(by_alias=True) for q in queries]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title=f"Saved Queries (Dataset {dataset_id})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@dataset.command("create-query")
@click.argument("dataset_id", type=int)
@click.option("--name", required=True, help="Query name")
@click.option("--sql", required=True, help="SQL query")
@click.option("--description", help="Query description")
@click.pass_context
def create_query(ctx, dataset_id, name, sql, description):
    """Create saved query."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        query = client.dataset.create_saved_query(
            dataset_id, name=name, sql=sql, description=description
        )
        print_json(query.model_dump(by_alias=True))
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@dataset.command("delete-query")
@click.argument("dataset_id", type=int)
@click.argument("query_id", type=int)
@click.pass_context
def delete_query(ctx, dataset_id, query_id):
    """Delete saved query."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        client.dataset.delete_saved_query(dataset_id, query_id)
        click.echo(f"Query {query_id} deleted successfully")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()
