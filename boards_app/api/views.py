from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boards_app.models import BoardsModel
from .serializers import BoardsSerializer, BoardDetailSerializer, BoardPatchSerializer
from .permissions import IsBoardOwnerOrMember


class BoardsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Kanban boards.

    Provides full CRUD operations for boards with additional
    filtering and aggregation logic.

    Features:
    - Users can only access boards they own or are members of
    - Automatic task statistics per board
    - Dynamic serializer selection based on action
    """
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            queryset = BoardsModel.objects.filter(Q(owner=user) | Q(members=user))
        else:
            queryset = BoardsModel.objects.all()
            
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('members', 'taskmodel_set')

        return queryset.annotate(
            member_count=Count('members', distinct=True),
            ticket_count=Count('taskmodel', distinct=True),
            tasks_to_do_count=Count(
                'taskmodel',
                filter=Q(taskmodel__status='to-do'),
                distinct=True
            ),
            tasks_high_prio_count=Count(
                'taskmodel',
                filter=Q(taskmodel__priority='high'),
                distinct=True
            ),
        ).distinct()
    
    def get_serializer_class(self):
        """
        Returns serializer based on action type.

        Actions:
        - retrieve -> detailed board view
        - partial_update -> patch serializer
        - default -> standard board serializer
        """
        if self.action == 'partial_update':
            return BoardPatchSerializer
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardsSerializer

    def perform_create(self,serializer):
        """
        Automatically assigns the authenticated user as board owner.
        """
        serializer.save(owner=self.request.user)

