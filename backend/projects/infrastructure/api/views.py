from rest_framework import generics, status, permissions
from rest_framework.response import Response
from dependency_injector.wiring import inject, Provide

from ...containers import ProjectContainer
from ...application.dtos import ProjectCreateDTO
from ...application.services import ProjectService
from .serializers import ProjectCreateSerializer, ProjectSerializer

class ProjectCreateAPIView(generics.GenericAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @inject
    def post(self, request, project_service: ProjectService = Provide[ProjectContainer.project_service]):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        create_dto = ProjectCreateDTO(
            owner_id=request.user.id,
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
            needed_skill_text=serializer.validated_data.get('needed_skill_text', '')
        )

        try:
            created_project_dto = project_service.create_project(create_dto)
            output_serializer = ProjectSerializer(created_project_dto)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 