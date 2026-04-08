import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legalcore.settings')

app = Celery('legalcore')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

