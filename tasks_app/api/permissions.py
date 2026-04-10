from rest_framework.permissions import BasePermission
from boards_app.models import BoardsModel
from rest_framework.exceptions import NotFound

class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Object-level permission for TaskModel.

    Grants access if:
    - the requesting user is the creator of the task, OR
    - the requesting user is the owner of the board the task belongs to.

    This ensures both task-level ownership and board-level administrative control.
    """
class IsTaskCreatorOrBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_member = obj.board.members.filter(id=request.user.id).exists()
        is_owner = obj.board.owner == request.user
        is_creator = obj.creator == request.user

        return is_member and (is_creator or is_owner)
    

class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        
        board_id = request.data.get('board')
        if not board_id:
            return NotFound("Board not provided.")
        
        try:
            board = BoardsModel.objects.get(id=board_id)
        except BoardsModel.DoesNotExist:
            raise NotFound(detail="Board not found.")
        
        is_member = board.members.filter(id=request.user.id).exists()
        is_owner = board.owner == request.user

        return is_member or is_owner