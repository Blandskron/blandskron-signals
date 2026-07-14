from rest_framework.permissions import BasePermission


class InternalAPIOnly(BasePermission):
    message = "Se requiere autenticación interna."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class RestrictedPublicationPermission(BasePermission):
    message = "La publicación requiere permisos explícitos."

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.data.get("state") not in {"published", "scheduled", "approved"} or bool(request.user and request.user.is_superuser)
