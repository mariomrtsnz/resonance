from dependency_injector.wiring import inject, Provide
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

from users.application.dtos import UserRegistrationDTO, UserDTO
from users.application.services import UserService, UserRegistrationError
from users.containers import UserContainer
from .serializers import UserRegistrationRequestSerializer, UserResponseSerializer

class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationRequestSerializer
    permission_classes = [permissions.AllowAny]

    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[UserContainer.user_service],
        *args,
        **kwargs
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        registration_dto = UserRegistrationDTO(
            email=validated_data['email'],
            password=validated_data['password']
        )

        try:
            user_dto: UserDTO = user_service.register_user(registration_dto)
            
            response_serializer = UserResponseSerializer(instance=user_dto)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except UserRegistrationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # TODO: Add proper logging for unexpected errors
            # logger.exception("Unexpected error during user registration") 
            return Response({"error": "An unexpected server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 