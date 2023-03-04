#!/bin/zsh
DJANGO_SETTINGS_MODULE=webapp.stage
.venv/bin/gunicorn --worker-class='gevent' --bind unix:/tmp/test-anna.sock webapp.wsgi:application
