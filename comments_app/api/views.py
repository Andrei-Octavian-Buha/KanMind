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
    """
    Handles listing and creating comments for a specific task.

    Permissions:
        - User must be authenticated
        - User must have access to the task (CanAccessTaskComments)

    Endpoints:
        GET    -> list all comments for a task
        POST   -> create a new comment for a task
    """
    permission_classes = [IsAuthenticated, CanAccessTaskComments]
    
    def get(self, request, task_id):
        """
        Retrieve all comments for a given task.

        Args:
            task_id (int): ID of the task

        Returns:
            list: Serialized comments
        """
        task = get_object_or_404(TaskModel, id=task_id)
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, task_id):
        """
        Create a new comment for a task.

        Args:
            task_id (int): ID of the task
            request.data: comment payload

        Returns:
            201: Created comment
            400: Validation errors
        """
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
    permission_classes = [IsAuthenticated, CanAccessTaskComments]
    """
    Handles deletion of a comment.

    Rules:
    - Only the author of the comment can delete it
    """
    def delete(self, request, task_id, comment_id):
        """
        Delete a comment if the user is the author.

        Args:
            task_id (int): ID of the related task
            comment_id (int): ID of the comment

        Returns:
            204: Deleted successfully
            403: Not allowed
        """
        task = get_object_or_404(TaskModel, id=task_id)
        comment = get_object_or_404(Comment,
                                    id=comment_id,
                                    task=task
                                    )
        if comment.author != request.user:
            return Response(
                {"detail":"Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
