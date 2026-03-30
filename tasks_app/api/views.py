from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from tasks_app.models import TaskModel
from .serializers import TaskSerializer
from .permissions import IsTaskCreatorOrBoardOwner

class TasksViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated, IsTaskCreatorOrBoardOwner]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=['get'],url_path='assigned-to-me')
    def assigned_to_me(self, request):
        user = request.user
        
        qs = TaskModel.objects.filter(assignee=user)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'],url_path='reviewing')
    def reviewing(self, request):
        user = request.user
        qs = TaskModel.objects.filter(reviewer=user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)