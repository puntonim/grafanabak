import datetime
import os
import json

import click
import requests
from slugify import slugify


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class BaseClass:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer {}".format(api_key)})
        self._org = None

    def _get_org(self):
        url = f"{self.base_url}/api/org/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    @property
    def org(self):
        if self._org is None:
            self._org = self._get_org()
        return self._org


class Backup(BaseClass):
    def __init__(self, api_key, base_url, project_name):
        self.base_url = base_url
        self.project_name = project_name
        super().__init__(api_key)

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
        title = dashboard_source["dashboard"]["title"]
        uid = dashboard_source["dashboard"]["uid"]
        click.echo(
            'Backing up "{}" - uid={} - org={}|{}'.format(
                title, uid, self.org["id"], slugify(self.org["name"])
            )
        )
        subdir_path = self._create_subdir()

        # Create the json file.
        file_name = "{}|{}.json".format(slugify(title), slugify(uid))
        file_path = os.path.join(subdir_path, file_name)
        with open(file_path, "w") as fout:
            fout.write(json.dumps(dashboard_source, indent=2))

    def _create_subdir(self):
        # Create project dir, if necessary.
        project_dir_path = os.path.join(BASE_DIR, "backups", self.project_name)
        if not os.path.exists(project_dir_path):
            os.makedirs(project_dir_path)
        # Create (sub)dir, if necessary.
        today = datetime.date.today()
        subdir_name = "org-{}-{}|{}|{}".format(
            self.org["id"],
            slugify(self.org["name"]),
            today.strftime("%Y-%m-%d"),
            slugify(self.base_url.split("://")[1].split("/")[0]),
        )
        subdir_path = os.path.join(project_dir_path, subdir_name)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
        return subdir_path


class Restore(BaseClass):
    def __init__(self, api_key, base_url, json_file_or_dir):
        self.base_url = base_url
        self.json_files = get_files(json_file_or_dir)
        super().__init__(api_key)

    def restore_dashboard(self, as_new=False):
        for json_file in self.json_files:
            click.echo(
                "Restoring {} - org={}|{}".format(
                    json_file, self.org["id"], slugify(self.org["name"])
                )
            )
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
        if os.path.isfile(fpath) and fpath.endswith("json"):
            result.append(fpath)
    return result

