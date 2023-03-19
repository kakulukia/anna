#!/bin/zsh
export DJANGO_SETTINGS_MODULE=settings.stage && .venv/bin/python manage.py run_huey
