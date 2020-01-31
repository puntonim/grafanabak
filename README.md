# Backup and restore Grafana dashboards

## API Keys
You need to generate one API key in Grafana for each Grafana organization and either:

_For `backup` command_:
- store all keys in a file named `api-keys.json` (see template `api-keys.json.TEMPLATE`)
- or use one key as env var `API_KEY`, eg:
    ```bash
    API_KEY=mykey python grafanabak.py backup...
    ```
_For `restore` command_:
- use one key as env var `API_KEY`, eg:
    ```bash
    API_KEY=mykey python grafanabak.py restore...
    ```
- or store all keys in a file named `api-keys.json` (see template `api-keys.json.TEMPLATE`)
and specify one, eg:
    ```bash
    API_KEY_ID=studio-bergamo-key python grafanabak.py restore...
    ```


## Usage
```bash
# First install the requirements:
$ pip install -r requirements/requirements-base.txt

## BACKUP
# Backup all dashboards:
$ python grafanabak.py backup http://turtle-grafana.web.cern.ch turtle-cern

## RESTORE
# Restore by updating the existing dashboard:
$ python grafanabak.py restore http://127.0.0.1:3000 ./backups/mierecensioni/subdir/file.json
# Restore all dashboards in a dir (updating):
$ python grafanabak.py restore http://127.0.0.1:3000 ./backups/mierecensioni/subdir
# Restore by creating a new dashboard:
$ python grafanabak.py restore-as-new http://127.0.0.1:3000 ./backups/mierecensioni/subdir/file.json
```


## Makefile
You can use Makefile shortcuts:
```bash
$ make backup/"http://dashboard.mierecensioni.it mierecensioni"
$ make restore/"http://127.0.0.1:3000 ./backups/mierecensioni/subdir/dash.json"
$ make restorenew/"http://127.0.0.1:3000 ./backups/mierecensioni/subdir/dash.json"
```
