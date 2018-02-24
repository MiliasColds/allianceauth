#!/usr/bin/env bash

# TODO route log output to file.
yes yes | python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
yes yes | python manage.py evolve --hint --execute

python manage.py shell < run_alliance_corp_update.py
celery -A alliance_auth beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach
celery -A alliance_auth worker -l info --detach
python manage.py celeryd &
python manage.py celerybeat &

python manage.py runserver 0.0.0.0:8000&

