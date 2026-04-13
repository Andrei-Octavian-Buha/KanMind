from rest_framework.permissions import BasePermission
from tasks_app.models import TaskModel
from django.db.models import Q
from rest_framework.exceptions import NotFound

class CanAccessTaskComments(BasePermission):
    """
    Permission that controls access to comments on a task.

    Rules:
    - User must be authenticated
    - User must have access to the parent task
      (either as board owner or board member)
    """
    def has_permission(self, request, view):
        """
        Checks if the user has permission to access comments
        for a specific task.

        Logic:
        - Extract task_id from URL
        - Validate that task exists
        - Ensure user is related to the board (owner or member)

        Returns:
            bool: True if access is allowed, False otherwise
        """
        task_id = view.kwargs.get("task_id")
        try: 
            task = TaskModel.objects.get(id=task_id)
        except TaskModel.DoesNotExist:
            return False
        is_member = task.board.members.filter(id=request.user.id).exists()
        is_owner = task.board.owner == request.user
        
        return is_member or is_owner