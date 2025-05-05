from django.urls import path
from .views import ProjectCreateAPIView

app_name = 'projects_api'

urlpatterns = [
    path('', ProjectCreateAPIView.as_view(), name='project-create'),
] 