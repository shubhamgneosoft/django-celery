import os

from celery import Celery

# Setting the Default Django settings module
from . import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app=Celery('mysite')

# Using a String here means the worker will always find the configuration information
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

