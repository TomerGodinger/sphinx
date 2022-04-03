import click
from .commands import starter
from .commands import main

@click.group(invoke_without_command=True)
def cli():
    """Your standard, everyday lunch CLI."""
    pass

cli.add_command(starter.starter_group)
cli.add_command(main.main_group)
