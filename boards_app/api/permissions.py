from rest_framework.permissions import BasePermission

class IsBoardOwnerOrMember(BasePermission):
    """
    Permission that allows access only to board owners or board members.

    Rules:
    - Access is granted if the user is the board owner
    - OR if the user is included in the board members list
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        """
        Checks object-level permission for a board instance.

        Args:
            request: HTTP request containing authenticated user
            view: DRF view instance
            obj: BoardsModel instance

        Returns:
            bool: True if user has access, False otherwise
        """
        return (
            obj.owner_id == request.user.id or 
            obj.members.filter(id=request.user.id).exists()
        )