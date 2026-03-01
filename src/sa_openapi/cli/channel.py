"""Channel CLI commands."""

import click

from ..client import SensorsAnalyticsClient
from .output import print_error, print_json, print_table


@click.group()
def channel():
    """Channel commands."""
    pass


@channel.command("list")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_channels(ctx, output_format):
    """List all channels."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        channels = client.channel.list_channel()

        data = [c.model_dump(by_alias=True) for c in channels]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title="Channels")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@channel.command("list-links")
@click.option("--channel-id", required=True, type=int, help="Channel ID")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_links(ctx, channel_id, output_format):
    """List links for a channel."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        links = client.channel.list_link(channel_id=channel_id)

        data = [l.model_dump(by_alias=True) for l in links]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title=f"Links (Channel {channel_id})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@channel.command("get-link")
@click.argument("link_id", type=int)
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_link(ctx, link_id, output_format):
    """Get link details."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        link = client.channel.get_link(link_id)

        data = link.model_dump(by_alias=True)

        if output_format == "json":
            print_json(data)
        else:
            print_table([data], title=f"Link {link_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()


@channel.command("link-data")
@click.argument("link_id", type=int)
@click.option("--start-date", required=True, help="Start date (YYYY-MM-DD)")
@click.option("--end-date", required=True, help="End date (YYYY-MM-DD)")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table")
@click.pass_context
def get_link_data(ctx, link_id, start_date, end_date, output_format):
    """Get link data."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        data = client.channel.get_link_data(
            link_id,
            {"startDate": start_date, "endDate": end_date},
        )

        rows = []
        for row in data.rows:
            rows.append(dict(zip(data.columns, row)))

        if output_format == "json":
            print_json(rows)
        elif output_format == "csv":
            from .output import print_csv
            print_csv(rows)
        else:
            print_table(rows, title=f"Link {link_id} Data")
    except Exception as e:
        print_error(str(e))
        raise click.Abort()
