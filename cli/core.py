import sys
import click
from .commands import starter
from .commands import main

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, default=False,
              help='Display CLI version.')
def cli(version: bool):
    """Your standard, everyday lunch CLI."""
    if version:
        click.echo("CLI version: 1.33.7")

cli.add_command(starter.starter_group)
cli.add_command(main.main_group)

# Problem: You can't find anything in the index for commands
# or groups that don't have any options
# @cli.command()
# def unindexed():
#     """Can't see me in the index, can you?"""
#     click.echo("Peekabee, you can't see me!")
