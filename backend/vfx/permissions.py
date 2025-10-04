from rest_framework.permissions import BasePermission

class IsPostProdOrAssigned(BasePermission):
    """
    Allows access only to users with POST_PROD role or if they are part of the assigned team.
    NOTE: This is a basic implementation. A real-world scenario would use a more robust team/group check.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role in ['ADMIN', 'POST_PROD']:
            return True
        
        # This check is simplified; it assumes the user's username might match the team name.
        # A better implementation would involve a User-Team relationship.
        vfx_shot = getattr(obj, 'vfx_shot', obj) # Handle both VFXShot and ShotVersion objects
        return vfx_shot.assigned_team == user.username