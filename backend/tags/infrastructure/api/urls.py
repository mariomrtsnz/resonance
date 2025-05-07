from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet

app_name = 'tags_api'

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include(router.urls)),
]