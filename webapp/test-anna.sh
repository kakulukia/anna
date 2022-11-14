#!/bin/zsh
DJANGO_SETTINGS_MODULE=webapp.stage
.venv/bin/gunicorn --timeout 200 --access-logfile - --workers 3 --bind unix:/tmp/test-anna.sock webapp.wsgi:application
