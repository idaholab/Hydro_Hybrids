#! /bin/bash

gunicorn --bind 0.0.0.0:80 wsgi:app --log-level debug --timeout 1500