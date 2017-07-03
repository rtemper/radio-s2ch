from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery(
    app='backend',
    broker='redis://%s:6379/0' % os.environ.get('R_CELERY_BROKER_HOST', 'localhost')
)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
