#!/bin/zsh
.venv/bin/gunicorn --timeout 200 --access-logfile - --workers 3 --bind unix:/tmp/test-anna.sock webapp.wsgi:application
