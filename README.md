# Backup and restore Grafana dashboards

Usage:
```bash
$ pip install -r requirements/requirements-base.txt
$ API_KEY=mykey python grafanabak.py backup http://turtle-grafana.web.cern.ch
# Or with the Makefile:
$ make venv
$ API_KEY=mykey make backup/http://turtle-grafana.web.cern.ch
```
