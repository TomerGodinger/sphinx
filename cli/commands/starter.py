import click

@click.group(name='starter')
def starter_group():
    """Order a side dish."""
    pass


@starter_group.command()
@click.option('--yes', 'auto_confirm', is_flag=True)
def order_bread(auto_confirm: str):
    """Orders a bread dish."""
    if auto_confirm or click.confirm("Are you sure you'd like to order some bread?"):
        click.echo(f'Some bread here please!')


@starter_group.command()
@click.option('--sassiness-level', type=int, help='How rude you wish to be. Can be dangerous.')
def order_soup(sassiness_level: int, quantity: int):
    """
    Orders a serving of soup. Be polite or you might get banned.
    
    Soup goes great with `meat <cli-main.html#main-order-meat>`_, you know.

    Not so sure about `pastas <cli-main.html#main-order-pastas>`_ though.

    Be sure to specify a good :option:`dish <main-order-meat -dish>` though.
    """
    if sassiness_level > 5:
        click.echo('Soup Chef: "No soup for you! Come back, one year!"')
    else:
        click.echo('One bowl of soup please.')
