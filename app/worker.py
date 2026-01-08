import os
import time

from celery import Celery, signals
from app.config import settings
from tortoise import Tortoise


celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


#add modules to autodiscover
celery.autodiscover_tasks([app.module for app in settings.APP_MODULES])
