from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.utils.timezone import now,timedelta
from celery.utils.log import get_task_logger
from django.conf import settings
#from DirectoryListing.models import FileRepository
from datetime import datetime

import django

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileRepo.settings")
django.setup()


app = Celery('FileRepo', broker="redis://localhost:6379")
#logger = get_task_logger(__name__)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings',namespace="CELERY")
app.autodiscover_tasks()

@app.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    # Archive files after every few days
    sender.add_periodic_task(crontab(day_of_week="*/5"), archive_files.s(), name = "archive old file")
    #sender.add_periodic_task(10.0, debug_task.s(), name='add test every 10')


@app.task
def archive_files():
    archive_days=5
    from DirectoryListing.models import FileRepository
    print('Request: {0!r}'.format("request"))
    old_files = FileRepository.objects.filter(creation_time__gte=now() - timedelta(days=archive_days))
    for old_file in old_files:
        old_file.archived = True
        old_file.archived_date = now()
        old_file.save()