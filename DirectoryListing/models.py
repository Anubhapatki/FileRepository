from django.db import models
from django.utils.timezone import now


# Create your models here.
class FileRepository(models.Model):
    name = models.CharField(max_length=100)
    path = models.FilePathField()
    creation_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    size = models.IntegerField()
    archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField()

    class Meta:
        ordering = ["name"]
