"""Dashboard CLI commands."""

from typing import TYPE_CHECKING

import click

from .output import print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def dashboard():
    """Dashboard commands."""
    pass


@dashboard.command("list")
@click.option("--type", "nav_type", default="PRIVATE", help="Navigation type (PRIVATE or PUBLIC)")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_navigation(ctx, nav_type, output_format):
    """List dashboard navigations."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        navigations = client.dashboard.list_navigation(type=nav_type)

        data = [n.model_dump(by_alias=True) for n in navigations]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title=f"Navigations ({nav_type})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dashboard.command("bookmarks")
@click.option("--navigation-id", required=True, type=int, help="Navigation ID")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_bookmarks(ctx, navigation_id, output_format):
    """List bookmarks for a navigation."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        bookmarks = client.dashboard.list_bookmark(navigation_id=navigation_id)

        data = [b.model_dump(by_alias=True) for b in bookmarks]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title=f"Bookmarks (Navigation {navigation_id})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dashboard.command("get")
@click.argument("navigation_id", type=int)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_navigation(ctx, navigation_id, output_format):
    """Get navigation details."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        nav = client.dashboard.get_navigation(navigation_id)

        data = nav.model_dump(by_alias=True)

        if output_format == "json":
            print_json(data)
        else:
            print_table([data], title=f"Navigation {navigation_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dashboard.command("bookmark-data")
@click.argument("bookmark_id", type=int)
@click.option("--start-date", required=True, help="Start date (YYYY-MM-DD)")
@click.option("--end-date", required=True, help="End date (YYYY-MM-DD)")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table")
@click.pass_context
def get_bookmark_data(ctx, bookmark_id, start_date, end_date, output_format):
    """Get bookmark data."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        data = client.dashboard.get_bookmark_data(
            bookmark_id,
            {"startDate": start_date, "endDate": end_date},
        )

        # Convert to list of dicts
        rows = []
        for row in data.rows:
            rows.append(dict(zip(data.columns, row, strict=False)))

        if output_format == "json":
            print_json(rows)
        elif output_format == "csv":
            from .output import print_csv
            print_csv(rows)
        else:
            print_table(rows, title=f"Bookmark {bookmark_id} Data")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
