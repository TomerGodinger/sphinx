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
    click.echo(f'Pastas are a mustas! {quantity} servings of {dish} please!')

@main_group.command()
@click.option('-topping', metavar='<name>', envvar='TOPPING', default=None,
              show_default=True, help='What to put on the pizza')
def order_pizza(topping: str):
    """
    Orders tray of hot pizza.
    
    You can choose which topping to use with the :option:`-topping <main-order-pizza -topping>` option.
    We recommend the olives in particular; they go great on a pizza.
    """
    
    click.echo(f'One pizza please! And put some {topping[::-1]} on it please!')
