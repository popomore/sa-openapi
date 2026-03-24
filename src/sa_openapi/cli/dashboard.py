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
        navigations = client.dashboard.list_navigation(nav_type=nav_type)

        if output_format == "json":
            data = [n.model_dump(by_alias=True) for n in navigations]
            print_json(data)
        else:
            data = [
                {"id": n.id, "name": n.display_name, "dashboards": len(n.dashboards)}
                for n in navigations
            ]
            print_table(data, title=f"Navigations ({nav_type})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@dashboard.command("bookmarks")
@click.option("--type", "bookmark_type", default=None, help="Bookmark type filter")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_bookmarks(ctx, bookmark_type, output_format):
    """List all bookmarks."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        bookmarks = client.dashboard.list_bookmarks(bookmark_type=bookmark_type)

        if output_format == "json":
            data = [b.model_dump(by_alias=True) for b in bookmarks]
            print_json(data)
        else:
            data = [
                {
                    "id": b.id,
                    "name": b.name,
                    "type": b.type,
                    "create_time": b.create_time,
                }
                for b in bookmarks
            ]
            print_table(data, title="Bookmarks")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
