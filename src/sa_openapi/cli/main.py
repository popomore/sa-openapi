"""CLI main entry point."""

import click

from .._config import ConfigManager
from ..client import SensorsAnalyticsClient
from . import channel, config, dashboard, dataset, model


@click.group()
@click.option(
    "--profile",
    default="default",
    help="Configuration profile to use",
)
@click.option(
    "--base-url",
    help="Override base URL",
)
@click.option(
    "--api-key",
    help="Override API key",
)
@click.option(
    "--project",
    help="Override project",
)
@click.pass_context
def cli(ctx, profile, base_url, api_key, project):
    """Sensors Analytics CLI."""
    # If running config commands, no need for client
    if ctx.invoked_subcommand in ("config",):
        return

    # Get configuration
    manager = ConfigManager()
    cfg = manager.get_profile(profile)

    if not cfg:
        click.echo(f"Error: Profile '{profile}' not found. Run 'sa config init' first.", err=True)
        raise click.Abort()

    # Override with CLI options
    if base_url:
        cfg.base_url = base_url
    if api_key:
        cfg.api_key = api_key
    if project:
        cfg.project = project

    # Create client
    client = SensorsAnalyticsClient.from_config(cfg)
    ctx.obj = {"client": client}
    ctx.call_on_close(client.close)


# Register command groups
cli.add_command(dashboard.dashboard)
cli.add_command(channel.channel)
cli.add_command(dataset.dataset)
cli.add_command(model.model)
cli.add_command(config.config)


if __name__ == "__main__":
    cli()
