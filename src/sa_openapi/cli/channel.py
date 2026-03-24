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


@channel.command("campaigns")
@click.option("--page", default=1, type=int, help="Page number")
@click.option("--page-size", default=20, type=int, help="Page size")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_campaigns(ctx, page, page_size, output_format):
    """List all campaigns."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.channel.list_campaigns(page_num=page, page_size=page_size)

        if output_format == "json":
            print_json(result.model_dump(by_alias=True))
        else:
            data = [c.model_dump(by_alias=True) for c in result.campaign_details]
            print_table(data, title=f"Campaigns (total: {result.total_rows})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@channel.command("links")
@click.option("--page", default=1, type=int, help="Page number")
@click.option("--page-size", default=20, type=int, help="Page size")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def list_links(ctx, page, page_size, output_format):
    """List all channel links."""
    try:
        client: SensorsAnalyticsClient = ctx.obj["client"]
        result = client.channel.list_links(page_num=page, page_size=page_size)

        if output_format == "json":
            print_json(result.model_dump(by_alias=True))
        else:
            data = [
                {
                    "id": lk.id,
                    "name": lk.name,
                    "channel_type": lk.channel_type,
                    "device_type": lk.device_type,
                    "short_url": lk.short_url,
                }
                for lk in result.detail_results
            ]
            print_table(data, title=f"Channel Links (total: {result.total_rows})")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e


@channel.command("create-link")
@click.option(
    "--channel-type",
    required=True,
    help="渠道类型: app_normal, app_deeplink, web_normal, mina_normal, alipay_mini_track",
)
@click.option("--device-type", default="通用", help="设备类型, 默认: 通用")
@click.option("--app-address", help="推广页面地址 (APP 通用渠道)")
@click.option("--target-url", help="目标地址 (网页/小程序渠道)")
@click.option("--utm-source", help="utm_source 参数")
@click.option("--utm-medium", help="utm_medium 参数")
@click.option("--utm-campaign", help="utm_campaign 参数")
@click.option("--utm-term", help="utm_term 参数")
@click.option("--utm-content", help="utm_content 参数")
@click.option("--application-name", help="Deeplink 应用名称 (app_deeplink 类型必填)")
@click.option("--web-landing-page", help="网页落地页 (app_deeplink 类型)")
@click.option(
    "--json-input", "json_input", help="直接传入 JSON 格式的 channel_urls 列表 (会覆盖其他参数)"
)
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
        client: SensorsAnalyticsClient = ctx.obj["client"]

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
            summary = [
                {
                    "created": result.created,
                    "duplicated": result.duplicated,
                    "failed": result.failed,
                    "status": result.status,
                }
            ]
            print_table(summary, title="Create Link Result")
            if result.channel_urls:
                links = [
                    link.model_dump(by_alias=True, exclude_none=True)
                    for link in result.channel_urls
                ]
                print_table(links, title="Created Links")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
