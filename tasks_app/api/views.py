from rest_framework import viewsets
from tasks_app.models import TaskModel

class TasksViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()