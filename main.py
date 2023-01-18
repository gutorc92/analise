import click
from importers.funds_importers import import_funds
from producer.producer import producer_transactions
from analysis.basic_analysis import month_analysis

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command()  # @cli, not @click!
def sync():
    click.echo('Syncing')
    import_funds()

@cli.command()
def producer():
    click.echo('producing')
    producer_transactions()

@cli.command()
@click.option('--month', type=click.IntRange(1, 12))
@click.option('--year', type=click.Choice(['2022','2021']))
def analysis(month, year):
    print(month, year)
    click.echo('analysis')
    month_analysis(month, year)
if __name__ == '__main__':
    cli()