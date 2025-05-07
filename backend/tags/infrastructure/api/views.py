from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from dependency_injector.wiring import inject, Provide
from uuid import UUID

from ...application.services import SkillService
from ...containers import SkillContainer
from ...domain.exceptions import SkillAlreadyExistsError, SkillNotFoundError
from ...infrastructure.api.serializers import SkillCreateSerializer, SkillSerializer, SkillUpdateSerializer

class SkillViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @inject
    def __init__(self,
                 skill_service: SkillService = Provide[SkillContainer.skill_service],
                 **kwargs):
        self.skill_service = skill_service
        super().__init__(**kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]

    def create(self, request: Request) -> Response:
        if not request.user.is_staff and not request.user.is_superuser:
             return Response({"detail": "You do not have permission to perform this action."},
                             status=status.HTTP_403_FORBIDDEN)

        req_serializer = SkillCreateSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)
        
        skill_create_dto = req_serializer.save()

        try:
            created_skill_dto = self.skill_service.create_skill(skill_create_dto)
            res_serializer = SkillSerializer(created_skill_dto)
            return Response(res_serializer.data, status=status.HTTP_201_CREATED)
        except SkillAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # TODO: Log error
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self, request: Request) -> Response:
        skills_dtos = self.skill_service.get_all_skills()
        serializer = SkillSerializer(skills_dtos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: str = None) -> Response:
        try:
            skill_id = UUID(pk)
            skill_dto = self.skill_service.get_skill_by_id(skill_id)
            serializer = SkillSerializer(skill_dto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid skill ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except SkillNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # TODO: Log error
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request: Request, pk: str = None) -> Response:
        if not request.user.is_staff and not request.user.is_superuser:
             return Response({"detail": "You do not have permission to perform this action."},
                             status=status.HTTP_403_FORBIDDEN)

        req_serializer = SkillUpdateSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        skill_update_dto = req_serializer.to_dto() 

        try:
            skill_id = UUID(pk)
            updated_skill_dto = self.skill_service.update_skill(skill_id, skill_update_dto)
            res_serializer = SkillSerializer(updated_skill_dto)
            return Response(res_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid skill ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except SkillNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except SkillAlreadyExistsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # TODO: Log error
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request: Request, pk: str = None) -> Response:
        if not request.user.is_staff and not request.user.is_superuser:
             return Response({"detail": "You do not have permission to perform this action."},
                             status=status.HTTP_403_FORBIDDEN)
        try:
            skill_id = UUID(pk)
            self.skill_service.delete_skill(skill_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"detail": "Invalid skill ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except SkillNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # TODO: Log error
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)