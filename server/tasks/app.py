from celery import Celery
import os

app = Celery('celery', broker=os.environ.get('CELERY_BROKER', 'redis://redis:6379'),
             backend=os.environ.get('CELERY_BACKEND', 'redis://redis:6379'), include=['learning.refactor'])
