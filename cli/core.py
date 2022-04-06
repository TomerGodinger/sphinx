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
        click.echo("Fake LuCLI version: 1.33.7. This will match the documentation version in the real product.")

@click.command(name='call-waiter',
               short_help="Summons a waiter from the depths of Hell's kitchen.")
@click.option('--urgency', 'urgency', metavar='<LEVEL>', type=int, required=False, default=0, show_default=True, help='How urgently you need the waiter to come over')
def cmd_summon_waiter(urgency: int):
    """
    Calls forth a (hopefully) friendly waiter.

    Be sure to leave a nice tip when you leave if you enjoy their service!
    """
    click.echo(f"Waiter! We need you over here please! With {urgency} level(s) of urgency!")

cli.add_command(starter.starter_group)
cli.add_command(main.main_group)
cli.add_command(cmd_summon_waiter)

# Problem: You can't find anything in the index for commands
# or groups that don't have any options
# @cli.command()
# def unindexed():
#     """Can't see me in the index, can you?"""
#     click.echo("Peekabee, you can't see me!")
