"""EventMeta CLI commands."""

from typing import TYPE_CHECKING

import click

from .output import print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def event_meta():
    """Event metadata commands."""
    pass


@event_meta.command("events")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_events(ctx, output_format):
    """List all events."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        events = client.event_meta.list_events_all()

        if output_format == "json":
            print_json([e.model_dump(by_alias=True) for e in events])
        else:
            data = [
                {
                    "id": e.id,
                    "name": e.name,
                    "cname": e.cname,
                    "is_virtual": e.is_virtual,
                    "total_count": e.total_count,
                }
                for e in events
            ]
            print_table(data, title=f"Events ({len(events)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@event_meta.command("tags")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_tags(ctx, output_format):
    """List all event tags."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        tags = client.event_meta.list_event_tags()

        if output_format == "json":
            print_json([t.model_dump(by_alias=True) for t in tags])
        else:
            data = [{"id": t.id, "name": t.name, "color": t.color} for t in tags]
            print_table(data, title=f"Event Tags ({len(tags)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
