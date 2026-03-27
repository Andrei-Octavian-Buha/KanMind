from rest_framework import mixins, viewsets
from tasks_app.models import TaskModel
from .serializers import TaskSerializer

class TasksViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer