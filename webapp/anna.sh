#!/bin/zsh
.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/tmp/gunicorn.sock webapp.wsgi:application
