import datetime
import os
import json

import click
import requests

from .utils import slugify


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Backup(object):
    def __init__(self, api_key, base_url):
        self.base_url = base_url

        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer {}".format(api_key)})

    def bak_all_dashboards(self):
        dashboards = self._search_all_dashboards()
        for dashboard in dashboards:
            dashboard_source = self._get_dashboard(dashboard["uid"])
            self._write_dashboard_to_file(dashboard_source)

    def _search_all_dashboards(self):
        url = "{}/api/search?type=dash-db".format(self.base_url)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def _get_dashboard(self, uid):
        url = "{}/api/dashboards/uid/{}".format(self.base_url, uid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def _write_dashboard_to_file(self, dashboard_source):
        title_orig = dashboard_source["dashboard"]["title"]
        title = slugify(title_orig)
        uid = dashboard_source["dashboard"]["uid"]
        click.echo('Backing up "{}" - uid={}'.format(title_orig, uid))

        file_name = "{}-{}.json".format(title, uid)
        today = datetime.date.today()
        dir_name = "{}-{}".format(
            today.strftime("%Y-%m-%d"), self.base_url.split("://")[1].split("/")[0]
        )
        dir_path = os.path.join(BASE_DIR, "backups", dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, file_name)

        with open(file_path, "w") as fout:
            fout.write(json.dumps(dashboard_source, indent=2))


class Restore(object):
    def __init__(self, api_key, base_url, json_file_or_dir):
        self.base_url = base_url
        self.json_files = get_files(json_file_or_dir)

        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer {}".format(api_key)})

    def restore_dashboard(self, as_new=False):
        for json_file in self.json_files:
            click.echo("Restoring {}".format(json_file))
            with open(json_file) as fin:
                file_data = fin.read()
            file_data = json.loads(file_data)
            data = dict(dashboard=file_data["dashboard"])

            if as_new:
                data["dashboard"]["id"] = None
                data["dashboard"]["uid"] = None
            else:
                data["overwrite"] = True

            url = "{}/api/dashboards/db".format(self.base_url)
            response = self.session.post(url, json=data)
            response.raise_for_status()

            click.echo(response.json())


def get_files(json_file_or_dir):
    if os.path.isfile(json_file_or_dir):
        return [json_file_or_dir]

    # List all files in the dir.
    result = []
    for f in os.listdir(json_file_or_dir):
        fpath = os.path.join(json_file_or_dir, f)
        if os.path.isfile(fpath):
            result.append(fpath)
    return result

