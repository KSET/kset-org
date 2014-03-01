#!/bin/bash
set -e

source /home/`whoami`/.virtualenvs/kset/bin/activate

export DJANGO_SETTINGS_MODULE=kset.settings


exec gunicorn -c gunicorn_config.py kset.wsgi:kset

