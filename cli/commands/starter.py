from ..clickmod import click

@click.group(name='starter')
def starter_group():
    """Order a starter dish."""
    pass


@starter_group.command(name='order-bread',
                       short_help='Order doughy goodness.')
@click.option('--yes', 'auto_confirm', is_flag=True, help='No? No, no no. Yes.')
def order_bread(auto_confirm: str):
    """Orders a bread dish."""
    if auto_confirm or click.confirm("Are you sure you'd like to order some bread?"):
        click.echo(f'Some bread here please!')

#Soup goes great with `meat <cli-main.html#main-order-meat>`_, you know (just be sure to specify a good :option:`dish <main order-meat -dish>`).
@starter_group.command(name='order-soup',
                       short_help='Order some hot, hot soup.')
@click.option('--sassiness-level', '-s', type=int, help='How rude you wish to be. Can be dangerous.')
def order_soup(sassiness_level: int):
    """
    Orders a serving of soup. Be polite or you might get banned.
    
    Soup goes great with :ref:`meat <main-order-meat>`, you know (just be sure to specify a good :option:`dish <main order-meat -dish>`).

    Not so sure about :ref:`pastas <main-order-pastas>` though.

    Well, just go look at the :ref:`main <main>` group in general.
    """
    if sassiness_level > 5:
        click.echo('Soup Chef: "No soup for you! Come back, one year!"')
    else:
        click.echo('One bowl of soup please.')

@starter_group.command(name='order-salad',
                       short_help='Orders an intentionally unsorted array of vegetables.')
def order_salad():
    """
    Orders a mix of vegetables.

    Their order is random since it's a salad.
    Therefore we've decided that the vegetables themselves shall be random too.

    In other words, you don't get to pick anything here.
    Take it or leave it.

    Hey, we can use easy references now!
    Like `main` and `starter order-soup --sassiness-level` and `main order-meat dish`!
    """
    click.echo('Waiter: You get a bowl full of lettuce. This was chosen randomly and fairly. If you keep trying over and over again, you may get something else. Someday.')
