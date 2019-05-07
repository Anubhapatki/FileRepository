from rest_framework import serializers
from .models import FileRepository


class FileRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRepository
        fields = ('name', 'creation_time', 'modified_time', 'size', 'path')