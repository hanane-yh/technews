from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import environ

env = environ.Env()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technews.settings')

app = Celery(
    'technews',
    broker=f"amqp://{env('BROKER_USER')}:{env('BROKER_PASSWORD')}@{env('BROKER_IP')}:{env('BROKER_PORT')}/",
    backend='rpc://'
)

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
