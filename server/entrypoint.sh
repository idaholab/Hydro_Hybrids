#! /bin/bash

./celery.sh && gunicorn app:app -b 0.0.0.0:5000