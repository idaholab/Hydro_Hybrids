#! /bin/bash

/bin/bash celery.sh && gunicorn --bind 0.0.0.0:80 wsgi:app