from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from tags.domain.exceptions import SkillAlreadyExistsError, SkillNotFoundError
from projects.domain.exceptions import ProjectNotFoundError
from users.domain.exceptions import UserRegistrationError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If the default handler handled it (e.g., DRF's APIException, ValidationError), return that response
    if response is not None:
        return response

    # Handle specific custom exceptions
    if isinstance(exc, ProjectNotFoundError):
        return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)
    
    if isinstance(exc, UserRegistrationError):
        return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    
    if isinstance(exc, SkillNotFoundError):
        return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, SkillAlreadyExistsError):
        return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    # Handle Django's Http404 (if it wasn't caught by DRF default handler for some reason)
    if isinstance(exc, Http404):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # TODO: If it's an unhandled exception, log it
    # logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Let Django handle other exceptions (will result in 500)
    return None 