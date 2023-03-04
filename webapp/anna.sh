#!/bin/zsh
.venv/bin/gunicorn --worker-class='gevent' --bind unix:/tmp/anna.sock webapp.wsgi:application
