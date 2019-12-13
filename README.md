# Backup and restore Grafana dashboards

## API Key
You need to generate an API Key in Grafana and either:
- store it in a file named `api-key`
- use it as env var `API_KEY`, eg:
    ```bash
    API_KEY=mykey python grafanabak.py ...
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
$ make backup/"http://turtle-grafana.web.cern.ch turtle-cern"
$ make restore/"http://127.0.0.1:3000 ./backups/mierecensioni/subdir/dash.json"
$ make restorenew/"http://127.0.0.1:3000 ./backups/mierecensioni/subdir/dash.json"
```
