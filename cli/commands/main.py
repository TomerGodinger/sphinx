import click

@click.group(name='main')
def main_group():
    """Order a main dish."""
    pass


@main_group.command()
@click.option('-dish', metavar='<name>', envvar='DISH', default='burger',
                show_default=True, help='The meat dish to order')
def order_meat(when: str, dish: str):
    """Orders a meat dish."""
    click.echo(f'Meat is neat! One {dish} please!')


@main_group.command()
@click.option('-dish', metavar='<name>', envvar='DISH', default='penne',
              show_default=True, help='The type of pastas to order')
@click.option('-quantity', metavar='<quantity>', default=5,
              show_default=True, help='The amount of pasta dishes to order')
def order_pastas(dish: str, quantity: int):
    """
    Orders a bunch of pasta dishes.
    
    Note that it is possible - and even recommended - to order
    a pasta and also order meat via the `meat <#main-order-meat>`_ command.

    The :option:`order-pastas -dish <main-order-pastas -dish>` argument for this command is similar to the
    :option:`meat -dish <main-order-meat -dish>` argument in the one above.
    """
    click.echo('Pastas are a mustas! {quantity} servings of {dish} please!')
