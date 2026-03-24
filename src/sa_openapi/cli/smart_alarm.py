"""SmartAlarm CLI commands."""

from typing import TYPE_CHECKING

import click

from .output import console, print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


@click.group()
def smart_alarm():
    """Smart alarm commands."""
    pass


@smart_alarm.command("get")
@click.argument("config_id", type=int)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_alarm_config(ctx, config_id, output_format):
    """Get a smart alarm configuration detail.

    CONFIG_ID: Alarm configuration ID
    """
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        alarm = client.smart_alarm.get_alarm_config(config_id)

        if output_format == "json":
            print_json(alarm.model_dump(by_alias=True))
        else:
            data = {
                "id": alarm.id,
                "title": alarm.title,
                "unit": alarm.unit,
                "send_alarm": alarm.send_alarm,
                "emails": ", ".join(alarm.emails),
            }
            print_table([data], title=f"Smart Alarm {config_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@smart_alarm.command("list")
@click.option("--title", help="Filter by title")
@click.option("--units", multiple=True, help="Filter by units (can be repeated)")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_alarms(ctx, title, units, output_format):
    """List all smart alarms."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        params: dict = {}
        if title:
            params["title"] = title
        if units:
            params["units"] = list(units)

        result = client.smart_alarm.list_alarms(params if params else None)

        if output_format == "json":
            print_json(result.model_dump(by_alias=True))
        else:
            console.print("\n[bold]Smart Alarms[/bold]")
            console.print(f"  Total: {result.total}")
            console.print(f"  IDs: {result.ids}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
