import os

import click

from domain.models import Backup, Restore


@click.group()
def cli():
    pass


@click.command()
@click.argument('url')
def backup(url):
    api_key = get_api_key()
    bak = Backup(api_key, url)
    bak.bak_all_dashboards()


@click.command()
@click.argument('url')
@click.argument('json_file', type=click.File('r'))
def restore(url, json_file):
    api_key = get_api_key()
    restore = Restore(api_key, url, json_file)
    restore.restore_dashboard()


def get_api_key():
    # API_KEY as environment var and not as args for security reason.
    api_key = os.environ.get('API_KEY')
    if not api_key:
        click.echo('Error: API_KEY environment var not available')
    return api_key


cli.add_command(backup)
cli.add_command(restore)


if __name__ == '__main__':
    click.echo('** GRAFANABAK **')
    cli()
