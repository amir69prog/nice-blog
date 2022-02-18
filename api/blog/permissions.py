from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
        Permission for post_detail view to check the user that has been seen the view is author or not
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True # ReadOnly
        
        return obj.author == request.user