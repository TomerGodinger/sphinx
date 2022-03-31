import click

@click.group()
def cli():
    """Your standard, everyday lunch CLI."""
    pass


@cli.command()
@click.option('-dish', metavar='thing', envvar='DISH', default='burger',
                show_default=True, help='The meat dish to order')
def order_meat(dish: str):
    """Orders a meat dish."""
    click.echo(f'Meat is neat! One {dish} please!')


@cli.command()
@click.option('-dish', metavar='<thang>', envvar='DISH', default='penne',
              show_default=True, help='The type of pastas to order')
@click.option('-quantity', metavar='<quantity>', default=5,
              show_default=True, help='The amount of pasta dishes to order')
def order_pastas(dish: str, quantity: int):
    """Orders a bunch of pasta dishes."""
    click.echo('Pastas are a mustas! {quantity} servings of {dish} please!')
