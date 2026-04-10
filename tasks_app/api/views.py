from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from tasks_app.models import TaskModel
from .serializers import TaskSerializer
from .permissions import IsTaskCreatorOrBoardOwner,IsBoardMember

class TasksViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet for managing tasks.

    Provides:
    - Retrieve task details
    - Create new tasks
    - Update existing tasks
    - Delete tasks

    Additional endpoints:
    - assigned-to-me
    - reviewing
    """
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated, IsBoardMember, IsTaskCreatorOrBoardOwner]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsBoardMember()]
        if self.action in ['retrive', 'update','partial_update','destroy']:
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated()]
    def get_queryset(self):
        """
        User can see only the tasks were he is member
        """
        return TaskModel.objects.filter(board__members=self.request.user).distinct()
    
    def perform_create(self, serializer):
        """
        Automatically assigns the authenticated user as task creator.
        """
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=['get'],url_path='assigned-to-me')
    def assigned_to_me(self, request):
        """
        Returns tasks assigned to the authenticated user.
        """
        user = request.user
        
        qs = TaskModel.objects.filter(assignee=user)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'],url_path='reviewing')
    def reviewing(self, request):
        """
        Returns tasks where the authenticated user is reviewer.
        """
        user = request.user
        qs = TaskModel.objects.filter(reviewer=user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)