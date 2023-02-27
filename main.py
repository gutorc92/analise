import click
import os
import subprocess
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
    directory = os.path.dirname(os.path.abspath(__file__))
    import_funds(directory)

@cli.command()
def producer():
    click.echo('producing')
    directory = os.path.dirname(os.path.abspath(__file__))
    producer_transactions(directory)

@cli.command()
@click.option('--month', type=click.IntRange(1, 12))
@click.option('--year', type=click.Choice(['2022','2021']))
def analysis(month, year):
    print(month, year)
    click.echo('analysis')
    directory = os.path.dirname(os.path.abspath(__file__))
    month_analysis(month, year, directory)

@cli.command()
def remove_db():
    subprocess.Popen('rm transaction.db', shell=True)

@cli.command()
def create_db():
    subprocess.Popen('sqlite3 transaction.db "VACUUM;"', shell=True)
    print('created')

if __name__ == '__main__':
    cli()