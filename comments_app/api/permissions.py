from rest_framework.permissions import BasePermission
from tasks_app.models import TaskModel
from django.db.models import Q

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
        if not request.user.is_authenticated:
            return False

        task_id = view.kwargs.get("task_id")

        return TaskModel.objects.filter(
            id=task_id
        ).filter(
            Q(board__members=request.user) |
            Q(board__owner=request.user)
        ).exists()