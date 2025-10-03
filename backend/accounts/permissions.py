from rest_framework.permissions import BasePermission

class RoleRequiredPermission(BasePermission):
    def __init__(self, roles=None):
        self.roles = roles or []

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role in self.roles

def role_required(roles):
    class _RoleRequired(RoleRequiredPermission):
        def __init__(self):
            super().__init__(roles)
    return _RoleRequired