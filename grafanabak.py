import os

import click

from domain.models import Backup, Restore


@click.group()
def cli():
    pass


@click.command()
@click.argument("url")
def backup(url):
    api_key = get_api_key()
    bak = Backup(api_key, url)
    bak.bak_all_dashboards()


@click.command()
@click.argument("url")
# @click.argument("json_file", type=click.File("r"))  # `File` accepts only a file (and opens it).
@click.argument("json_file_or_dir", type=click.Path(exists=True))
def restore(url, json_file_or_dir):
    api_key = get_api_key()
    restore = Restore(api_key, url, json_file_or_dir)
    restore.restore_dashboard()


@click.command()
@click.argument("url")
@click.argument("json_file_or_dir", type=click.Path(exists=True))
def restore_as_new(url, json_file_or_dir):
    api_key = get_api_key()
    restore = Restore(api_key, url, json_file_or_dir)
    restore.restore_dashboard(as_new=True)


def get_api_key():
    # First get the API_KEY env var, if present.
    api_key = os.environ.get("API_KEY")
    # If not found, get the key from the file `api-key`.
    if not api_key:
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api-key")
        with open(fpath, "r") as fin:
            api_key = fin.read()
    if not api_key:
        click.echo(
            "Error: api key not found in `api-key` file nor API_KEY env var not available"
        )
    return api_key


cli.add_command(backup)
cli.add_command(restore)
cli.add_command(restore_as_new)


if __name__ == "__main__":
    click.echo("** GRAFANABAK **")
    cli()
