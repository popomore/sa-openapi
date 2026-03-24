"""Channel CLI commands."""

import json
from typing import TYPE_CHECKING

import click

from .output import print_error, print_json, print_table

if TYPE_CHECKING:
    from ..client import SensorsAnalyticsClient


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
        raise click.Abort() from e


@channel.command("list-links")
@click.option("--channel-id", required=True, type=int, help="Channel ID")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_links(ctx, channel_id, output_format):
    """List links for a channel."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        links = client.channel.list_link(channel_id=channel_id)

        data = [link.model_dump(by_alias=True) for link in links]

        if output_format == "json":
            print_json(data)
        else:
            print_table(data, title=f"Links (Channel {channel_id})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


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
        raise click.Abort() from e


@channel.command("link-data")
@click.argument("link_id", type=int)
@click.option("--start-date", required=True, help="Start date (YYYY-MM-DD)")
@click.option("--end-date", required=True, help="End date (YYYY-MM-DD)")
@click.option(
    "--format", "output_format", type=click.Choice(["table", "json", "csv"]), default="table"
)
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
            rows.append(dict(zip(data.columns, row, strict=False)))

        if output_format == "json":
            print_json(rows)
        elif output_format == "csv":
            from .output import print_csv

            print_csv(rows)
        else:
            print_table(rows, title=f"Link {link_id} Data")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@channel.command("create-link")
@click.option("--channel-type", required=True, help="渠道类型: app_normal, app_deeplink, web_normal, mina_normal, alipay_mini_track")
@click.option("--device-type", default="通用", help="设备类型，默认：通用")
@click.option("--app-address", help="推广页面地址（APP 通用渠道）")
@click.option("--target-url", help="目标地址（网页/小程序渠道）")
@click.option("--utm-source", help="utm_source 参数")
@click.option("--utm-medium", help="utm_medium 参数")
@click.option("--utm-campaign", help="utm_campaign 参数")
@click.option("--utm-term", help="utm_term 参数")
@click.option("--utm-content", help="utm_content 参数")
@click.option("--application-name", help="Deeplink 应用名称（app_deeplink 类型必填）")
@click.option("--web-landing-page", help="网页落地页（app_deeplink 类型）")
@click.option("--json-input", "json_input", help="直接传入 JSON 格式的 channel_urls 列表（会覆盖其他参数）")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def create_link(
    ctx,
    channel_type,
    device_type,
    app_address,
    target_url,
    utm_source,
    utm_medium,
    utm_campaign,
    utm_term,
    utm_content,
    application_name,
    web_landing_page,
    json_input,
    output_format,
):
    """Create channel tracking link(s)."""
    try:
        client: "SensorsAnalyticsClient" = ctx.obj["client"]

        if json_input:
            channel_urls = json.loads(json_input)
        else:
            parameters: dict = {}
            if utm_source:
                parameters["utm_source"] = utm_source
            if utm_medium:
                parameters["utm_medium"] = utm_medium
            if utm_campaign:
                parameters["utm_campaign"] = utm_campaign
            if utm_term:
                parameters["utm_term"] = utm_term
            if utm_content:
                parameters["utm_content"] = utm_content

            item: dict = {"channel_type": channel_type, "device_type": device_type}
            if app_address:
                item["app_address"] = app_address
            if target_url:
                item["target_url"] = target_url
            if application_name:
                item["application_name"] = application_name
            if web_landing_page:
                item["web_landing_page"] = web_landing_page
            if parameters:
                item["parameters"] = parameters
            channel_urls = [item]

        result = client.channel.create_link(channel_urls)

        if output_format == "json":
            print_json(result.model_dump(by_alias=True, exclude_none=True))
        else:
            summary = [{"created": result.created, "duplicated": result.duplicated, "failed": result.failed, "status": result.status}]
            print_table(summary, title="Create Link Result")
            if result.channel_urls:
                links = [link.model_dump(by_alias=True, exclude_none=True) for link in result.channel_urls]
                print_table(links, title="Created Links")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
