from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technews.settings')

app = Celery(
    'technews',
    broker=f"amqp://{os.getenv('BROKER_USER')}:{os.getenv('BROKER_PASSWORD')}@{os.getenv('BROKER_IP')}:{os.getenv('BROKER_PORT')}/",
    backend='rpc://'
)

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
