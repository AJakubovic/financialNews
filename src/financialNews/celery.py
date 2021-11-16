from celery import Celery
import os
import django
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "financialNews.settings")

django.setup()

app = Celery('feeds', broker='amqp://postgres:postgres@rabbit:5672') # url za brokera: RabbitMQ
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks() # registrira taskove unutar task modula u svakoj app iz INSTALLED_APPS
