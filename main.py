import click
import os
import logging
import subprocess
from importers.funds_importers import import_funds, import_stocks
from producer.producer import producer_transactions
from analysis.basic_analysis import month_analysis
from models import ASSET_TYPES
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    if debug:
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

@cli.command()  # @cli, not @click!
@click.option('--types', type=click.Choice(ASSET_TYPES, case_sensitive=False),  multiple=True, default=ASSET_TYPES)
def sync(types):
    click.echo('Syncing')
    directory = os.path.dirname(os.path.abspath(__file__))
    import_funds(directory, types)
    import_stocks(directory)
    

@cli.command()
def producer():
    click.echo('producing')
    directory = os.path.dirname(os.path.abspath(__file__))
    producer_transactions(directory)

@cli.command()
def consumer():
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