from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOptions(BasePermission):
    """
    The request type is OPTIONS
    """
    def has_permission(self, request, view):
        return request.method == 'OPTIONS'
