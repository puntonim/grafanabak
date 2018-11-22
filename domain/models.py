import click


class Backup(object):
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def bak_all_dashboards(self):
        click.echo('Backing up all dashboard at ' + self.base_url)
