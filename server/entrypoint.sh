#! /bin/bash

gunicorn --bind 0.0.0.0:80 wsgi:app --daemon & /bin/bash celery.sh