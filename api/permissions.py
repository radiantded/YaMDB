from rest_framework import permissions

ADMIN = 'admin'
MODERATOR = 'moderator'
DJANGO_ADMIN = 'django admin'


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == MODERATOR
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in (ADMIN, DJANGO_ADMIN)
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role in (ADMIN, DJANGO_ADMIN)
            )
        return False
