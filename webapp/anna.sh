#!/bin/zsh
.venv/bin/gunicorn webapp.wsgi:application --worker-class='gevent'
