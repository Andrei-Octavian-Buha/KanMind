from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer


class CreateNewTaskView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(owner=request.user)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TasksAssignedToMeView(generics.ListAPIView):
    pass