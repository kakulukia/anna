#!/bin/zsh
.venv/bin/gunicorn --env DJANGO_SETTINGS_MODULE=settings.stage --worker-class='gevent' --bind unix:/tmp/test-anna.sock webapp.wsgi:application
