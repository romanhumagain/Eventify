# # core/celery.py

# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# app = Celery('core')

# # Using a string here means the worker doesn’t have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Set Celery timezone to Nepal Time (Asia/Kathmandu)
# app.conf.timezone = 'Asia/Kathmandu'

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
