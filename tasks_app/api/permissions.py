from rest_framework.permissions import BasePermission
from boards_app.models import BoardsModel
class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Object-level permission for TaskModel.

    Grants access if:
    - the requesting user is the creator of the task, OR
    - the requesting user is the owner of the board the task belongs to.

    This ensures both task-level ownership and board-level administrative control.
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks whether the user can access or modify a specific task instance.

        Args:
            request: HTTP request containing authenticated user
            view: DRF view handling the request
            obj: TaskModel instance

        Returns:
            bool: True if access is allowed, False otherwise
        """
        return (
            obj.creator == request.user or
            obj.board.owner == request.user
        )
class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            board_id = request.data.get('board')
            if not board_id:
                return True
            return BoardsModel.objects.filter(id=board_id, members=request.user).exists()
        return True