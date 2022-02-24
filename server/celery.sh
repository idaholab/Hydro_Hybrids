#! /bin/bash

celery --app tasks.app worker --uid nobody --loglevel info --pool=prefork --concurrency=4 --max-tasks-per-child=1 --detach