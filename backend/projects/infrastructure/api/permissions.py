from rest_framework import permissions
import uuid

class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a project to view it.
    Assumes the object passed to has_object_permission has an 'owner_id'.
    """

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'owner_id'):
            return False

        if not isinstance(request.user.id, uuid.UUID):
             # Should not happen with the custom User model, but safeguard.
             return False

        return obj.owner_id == request.user.id 