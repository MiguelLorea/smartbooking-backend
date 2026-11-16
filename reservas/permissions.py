from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    message = "Solo el administrador puede hacer esto."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.rol == "admin")


class EsDuenioOAdmin(BasePermission):
    message = "No podes ver ni modificar reservas de otra persona."

    def has_object_permission(self, request, view, obj):
        if request.user.rol == "admin":
            return True
        return obj.usuario_id == request.user.id
