"""Config CLI commands."""

import click

from .._config import ClientConfig, ConfigManager
from .output import console, print_error, print_list, print_success


@click.group()
def config():
    """Configuration commands."""
    pass


@config.command("init")
@click.option("--base-url", prompt=True, help="Sensors Analytics base URL")
@click.option("--api-key", prompt=True, hide_input=True, help="API key")
@click.option("--project", prompt=True, default="default", help="Project name")
def init(base_url, api_key, project):
    """Initialize configuration interactively."""
    manager = ConfigManager()

    cfg = ClientConfig(
        base_url=base_url,
        api_key=api_key,
        project=project,
    )

    manager.save_profile("default", cfg)
    print_success(f"Configuration saved to {manager.config_path}")


@config.command("list")
def list_profiles():
    """List all profiles."""
    manager = ConfigManager()
    profiles = manager.list_profiles()
    print_list(profiles, title="Profiles")


@config.command("show")
@click.argument("profile", default="default")
def show_profile(profile):
    """Show profile configuration."""
    manager = ConfigManager()
    cfg = manager.get_profile(profile)

    if not cfg:
        print_error(f"Profile '{profile}' not found")
        return

    console.print(f"\n[bold]Profile: {profile}[/bold]")
    console.print(f"  Base URL: {cfg.base_url}")
    console.print(f"  API Key: {cfg.api_key[:10]}...")
    console.print(f"  Project: {cfg.project}")
    console.print(f"  Timeout: {cfg.timeout}s")
    console.print(f"  Max Retries: {cfg.max_retries}")


@config.command("set-default")
@click.argument("profile")
def set_default(profile):
    """Set default profile."""
    manager = ConfigManager()
    manager.set_default_profile(profile)
    print_success(f"Default profile set to '{profile}'")
