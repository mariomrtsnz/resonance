from dependency_injector.wiring import inject, Provide
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

from users.application.services import UserService, UserRegistrationError
from users.containers import UserContainer
from .serializers import UserRegistrationRequestSerializer, UserResponseSerializer

# Note: Views currently interact directly with serializers that use the ORM.
# Ideally, views would interact with the Application Service. But adding the
# DTOs layer would introduce mapping boilerplate that is unnecessary for this case
# since the API response structure closely matches the domain entities.
# Example:
# 1. View receives request data.
# 2. View calls Application Service (e.g., user_service.register_user(data)).
# 3. Service handles logic (validation, domain ops, repository calls).
# 4. Service returns result (e.g., domain User or DTO).
# 5. View uses a *different* serializer/mapper to format the result for the response.

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

        try:
            created_user = user_service.register_user(serializer.validated_data)
            
            response_data = {
                "id": created_user.id,
                "email": created_user.email,
                "username": created_user.username
            }
            response_serializer = UserResponseSerializer(instance=response_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except UserRegistrationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # TODO: Add proper logging for unexpected errors
            # logger.exception("Unexpected error during user registration") 
            return Response({"error": "An unexpected server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 