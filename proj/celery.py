from __future__ import absolute_import,unicode_literals
import os
from celery import Celery

# Setting the default django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE','proj.settings')

app = Celery('proj')

