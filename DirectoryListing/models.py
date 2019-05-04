from django.db import models


# Create your models here.
class FileRepository(models.Model):
    name = models.CharField(max_length=100)
    path = models.FilePathField()
    creation_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    size = models.IntegerField()

    class Meta:
        ordering = ["name"]
