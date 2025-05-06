from django.urls import path
from .views import ProjectCreateAPIView, ProjectListAPIView, ProjectRetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions

app_name = 'projects_api'

urlpatterns = [
    path('', ProjectListAPIView.as_view(), name='project-list'),
    path('', ProjectCreateAPIView.as_view(), name='project-create'),
]

class ProjectListCreateDispatchView(APIView):
    """Dispatches GET to List view and POST to Create view."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            view = ProjectRetrieveAPIView.as_view()
        else:
            view = ProjectListAPIView.as_view()
        return view(request._request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProjectCreateAPIView.as_view()
        return view(request._request, *args, **kwargs)

urlpatterns = [
    path('', ProjectListCreateDispatchView.as_view(), name='project-list-create'),
    path('<uuid:pk>/', ProjectRetrieveAPIView.as_view(), name='project-retrieve'),
] 