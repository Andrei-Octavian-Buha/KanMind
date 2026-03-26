from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boards_app.models import BoardsModel
from .serializers import BoardsSerializer, BoardDetailSerializer


class BoardsViewSet(viewsets.ModelViewSet):
    queryset = BoardsModel.objects.all()
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardsSerializer

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

