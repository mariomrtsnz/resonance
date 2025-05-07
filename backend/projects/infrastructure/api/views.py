from rest_framework.request import Request
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dependency_injector.wiring import inject, Provide
from uuid import UUID


from ...application.services import ProjectService
from ...containers import ProjectContainer
from ...domain.exceptions import ProjectNotFoundError
from .serializers import ProjectCreateSerializer, ProjectSerializer

class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @inject
    def __init__(self,
                 project_service: ProjectService = Provide[ProjectContainer.project_service],
                 **kwargs):
        self.project_service = project_service
        super().__init__(**kwargs)

    def create(self, request: Request) -> Response:
        req_serializer = ProjectCreateSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)
        
        project_create_dto = req_serializer.save()

        try:
            created_project_dto = self.project_service.create_project(
                project_data=project_create_dto,
                owner_id=request.user.id
            )
            res_serializer = ProjectSerializer(created_project_dto)
            return Response(res_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # TODO: Log error
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request: Request) -> Response:
        projects_dtos = self.project_service.get_all_projects()
        serializer = ProjectSerializer(projects_dtos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request: Request, pk: str = None) -> Response:
        try:
            project_id = UUID(pk)
            project_dto = self.project_service.get_project_by_id(project_id)
            serializer = ProjectSerializer(project_dto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid project ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except ProjectNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # TODO: Log error
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)