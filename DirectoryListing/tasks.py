import logging
from filerepository.FileRepo.celeryapp import app
from .models import FileRepository
from django.utils.timezone import now,timedelta

@app.task
def archive_old_files():
    print ("I am here")
    archive_days = 1
    old_files = FileRepository.objects.filter(creation_time__gte=now() - timedelta(days=archive_days))
    old_files.archive = True
    old_files.archived_date = now()
    old_files.save()


