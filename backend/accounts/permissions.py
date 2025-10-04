from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    """
    A permission class that checks if a user has one of the required roles.
    The view must have a `required_roles` attribute, which is a list of
    role strings.
    
    Example:
        class MyView(APIView):
            permission_classes = [RolePermission]
            required_roles = ['PRODUCER', 'DIRECTOR']
    """
    def has_permission(self, request, view):
        # Allow access if the user is not authenticated, so other permissions can handle it.
        if not request.user or not request.user.is_authenticated:
            return True

        # Admins have universal access.
        if request.user.role == 'ADMIN':
            return True

        # Get the list of required roles from the view.
        required_roles = getattr(view, 'required_roles', [])
        
        # If no roles are required, deny access by default for safety.
        if not required_roles:
            return False

        # Check if the user's role is in the required list.
        return request.user.role in required_roles