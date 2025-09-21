"""main entrypoint"""
import click
from . import commands

@click.group()
def cli() -> None:
    """A simple CLI note taking application."""

# Register all commands from commands.py
cli.add_command(commands.add)
cli.add_command(commands.lst)
cli.add_command(commands.view)
cli.add_command(commands.delete)
cli.add_command(commands.search)

if __name__ == "__main__":
    cli()
