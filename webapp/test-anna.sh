#!/bin/zsh
export DJANGO_SETTINGS_MODULE=settings.stage && .venv/bin/gunicorn --worker-class='gevent' --bind unix:/tmp/test-anna.sock webapp.wsgi:application
