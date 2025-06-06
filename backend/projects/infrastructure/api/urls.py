from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

app_name = 'projects_api'

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
