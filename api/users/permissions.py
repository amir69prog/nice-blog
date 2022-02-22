from rest_framework import permissions
from .messages import ViewMessages


class IsSelfOrReadOnly(permissions.BasePermission):
    """
        Permission for user_detail view to check the user is the current user
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # ReadOnly

        return obj == request.user


class IsUserVerified(permissions.BasePermission):
    message = ViewMessages.USER_IS_NOT_VERIFIED.value

    def has_permission(self, request, view):
        return request.user.is_verified
