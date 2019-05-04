from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FileRepository


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    model = FileRepository

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["FileRepository"] = FileRepository.objects.all().order_by('name')
        return context
