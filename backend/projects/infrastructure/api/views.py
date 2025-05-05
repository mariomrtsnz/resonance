from rest_framework import generics, status, permissions
from rest_framework.response import Response
from dependency_injector.wiring import inject, Provide

from ...containers import ProjectContainer
from ...application.dtos import ProjectCreateDTO
from ...application.services import ProjectService
from .serializers import ProjectCreateSerializer, ProjectSerializer

class ProjectCreateAPIView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @inject
    def __init__(self,
                 project_service: ProjectService = Provide[ProjectContainer.project_service],
                 **kwargs):
        self.project_service = project_service
        super().__init__(**kwargs)

    def perform_create(self, serializer):
        project_create_dto = ProjectCreateDTO(**serializer.validated_data)
        project_dto = self.project_service.create_project(
            project_data=project_create_dto,
            owner_id=self.request.user.id
        )
        
        self._created_project_dto = project_dto

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        output_serializer = ProjectSerializer(self._created_project_dto)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    @inject
    def __init__(self,
                 project_service: ProjectService = Provide[ProjectContainer.project_service],
                 **kwargs):
        self.project_service = project_service
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.project_service.get_all_projects()

# Add ProjectRetrieveAPIView, ProjectUpdateAPIView, ProjectDestroyAPIView later 