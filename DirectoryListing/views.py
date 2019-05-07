from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FileRepository
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FileRepositorySerializer


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    model = FileRepository

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["FileRepository"] = FileRepository.objects.all().order_by('name')
        return context


class AvailableFilesInRepository(APIView):
    def get(self, request, format=None):
        available_files = FileRepository.objects.filter(archived=False)
        serializer = FileRepositorySerializer(available_files,many = True)
        return Response(serializer.data)


class ArchivedFilesInRepository(APIView):
    def get(self, request, format=None):
        archived_files = FileRepository.objects.filter(archived=True)
        serializer = FileRepositorySerializer(archived_files,many = True)
        return Response(serializer.data)