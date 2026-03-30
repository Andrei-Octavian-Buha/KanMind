from rest_framework.permissions import BasePermission
from tasks_app.models import TaskModel
from django.db.models import Q

class CanAccessTaskComments(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        task_id = view.kwargs.get("task_id")

        return TaskModel.objects.filter(
            id=task_id
        ).filter(
            Q(board__members=request.user) |
            Q(board__owner=request.user)
        ).exists()