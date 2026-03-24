"""PropertyMeta CLI commands."""

from typing import TYPE_CHECKING

import click

from .output import print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def property_meta():
    """Property metadata commands."""
    pass


@property_meta.command("event-properties")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_all_event_properties(ctx, output_format):
    """List all event properties."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        props = client.property_meta.list_all_event_properties()

        if output_format == "json":
            print_json([p.model_dump(by_alias=True) for p in props])
        else:
            data = [
                {"id": p.id, "name": p.name, "cname": p.cname, "data_type": p.data_type}
                for p in props
            ]
            print_table(data, title=f"Event Properties ({len(props)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@property_meta.command("event-properties-by-events")
@click.argument("events", nargs=-1, required=True)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_event_properties(ctx, events, output_format):
    """List properties for specified events.

    EVENTS: One or more event names
    """
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.property_meta.list_event_properties(list(events))

        if output_format == "json":
            print_json([r.model_dump(by_alias=True) for r in result])
        else:
            rows = []
            for ewp in result:
                event_def = ewp.event_define
                event_name = event_def.get("name", "") if isinstance(event_def, dict) else ""
                for p in ewp.properties:
                    rows.append(
                        {
                            "event": event_name,
                            "property": p.name,
                            "cname": p.cname,
                            "data_type": p.data_type,
                        }
                    )
            print_table(rows, title="Event Properties")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@property_meta.command("user-properties")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_all_user_properties(ctx, output_format):
    """List all user properties."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        props = client.property_meta.list_all_user_properties()

        if output_format == "json":
            print_json([p.model_dump(by_alias=True) for p in props])
        else:
            data = [
                {"id": p.id, "name": p.name, "cname": p.cname, "data_type": p.data_type}
                for p in props
            ]
            print_table(data, title=f"User Properties ({len(props)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@property_meta.command("user-groups")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_user_groups(ctx, output_format):
    """List all user groups (分群)."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        groups = client.property_meta.list_user_groups()

        if output_format == "json":
            print_json([g.model_dump(by_alias=True) for g in groups])
        else:
            data = [
                {"id": g.id, "name": g.name, "cname": g.cname, "data_type": g.data_type}
                for g in groups
            ]
            print_table(data, title=f"User Groups ({len(groups)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@property_meta.command("user-tags")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_user_tags(ctx, output_format):
    """List user tags with directory structure."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        tags = client.property_meta.list_user_tags_with_dir()

        if output_format == "json":
            print_json([t.model_dump(by_alias=True) for t in tags])
        else:
            data = [
                {"name": t.name, "cname": t.cname, "data_type": t.data_type, "type": t.type}
                for t in tags
            ]
            print_table(data, title=f"User Tags ({len(tags)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@property_meta.command("property-values")
@click.option("--table-type", required=True, help="Table type (e.g. event, user)")
@click.option("--property-name", required=True, help="Property name")
@click.option("--limit", type=int, default=None, help="Max number of values")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_property_values(ctx, table_type, property_name, limit, output_format):
    """Get candidate values for a property."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        values = client.property_meta.get_property_values(table_type, property_name, limit)

        if output_format == "json":
            print_json(values)
        else:
            data = [{"value": v} for v in values]
            print_table(data, title=f"Values for {property_name} ({len(values)})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
