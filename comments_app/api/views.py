from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from comments_app.models import Comment
from .serializers import CommentSerializer
from .permissions import CanAccessTaskComments
from tasks_app.models import TaskModel


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanAccessTaskComments]
    def get(self, request, task_id):
        comments = Comment.objects.filter(task_id=task_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                task=task,
                author=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDeleteView(APIView):

    def delete(self, request, task_id, comment_id):
        comment = get_object_or_404(Comment,
                                    id=comment_id,
                                    task_id=task_id
                                    )
        if comment.author != request.user:
            return Response(
                {"detail":"Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
