from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boards_app.models import BoardsModel
from .serializers import BoardsSerializer, BoardDetailSerializer, BoardPatchSerializer
from .permissions import IsBoardOwnerOrMember


class BoardsViewSet(viewsets.ModelViewSet):
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_queryset(self):
        user = self.request.user
        return BoardsModel.objects.filter(
            Q(owner=user) | Q(members=user)
        ).annotate(
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
        if self.action == 'partial_update':
            return BoardPatchSerializer
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardsSerializer

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

