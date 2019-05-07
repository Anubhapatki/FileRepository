from django.urls import path
from .views import IndexView, AvailableFilesInRepository, ArchivedFilesInRepository
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', IndexView.as_view() ),
    path('available_files', AvailableFilesInRepository.as_view()),
    path('archived_files', ArchivedFilesInRepository.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)