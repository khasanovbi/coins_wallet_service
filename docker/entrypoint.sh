#!/usr/bin/env sh
set -ex

python /usr/src/coins_wallet_service/manage.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE}

gunicorn coins_wallet_service.wsgi:application --bind 0.0.0.0:8000 --log-level debug
