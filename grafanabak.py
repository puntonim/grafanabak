import json
import os
import sys

import click

from domain.models import Backup, Restore


@click.group()
def cli():
    pass


@click.command()
@click.argument("url")
@click.argument("project_name")
def backup(url, project_name):
    api_keys = get_api_keys()
    for api_key in api_keys:
        bak = Backup(api_key, url, project_name)
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
    api_key = os.environ.get("API_KEY", None)
    if api_key:
        return api_key

    # If not found, get the key from `api-keys.json` with id=API_KEY_ID.
    api_key_id = os.environ.get("API_KEY_ID", None)
    if api_key_id is None:
        click.echo("Error: either API_KEY or API_KEY_ID env vars are required")
        sys.exit(1)
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api-keys.json")
    with open(fpath, "r") as fin:
        data = fin.read()
    data = json.loads(data)

    api_key = None
    for key in data:
        if key["id"] == api_key_id:
            api_key = key["key"]
    if not api_key:
        click.echo(f"Error: id {api_key_id} not found in api-keys.json")
        sys.exit(1)
    return api_key


def get_api_keys():
    # First get the API_KEY env var, if present.
    api_key = os.environ.get("API_KEY", None)
    if api_key:
        return [api_key]

    # If not found, get the keys from `api-keys.json`.
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api-keys.json")
    with open(fpath, "r") as fin:
        data = fin.read()
    data = json.loads(data)

    api_keys = []
    for key in data:
        api_keys.append(key["key"])
    return api_keys


cli.add_command(backup)
cli.add_command(restore)
cli.add_command(restore_as_new)


if __name__ == "__main__":
    click.echo("** GRAFANABAK **")
    cli()
