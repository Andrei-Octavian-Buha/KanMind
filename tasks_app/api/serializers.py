from rest_framework import serializers
from tasks_app.models import TaskModel
from django.contrib.auth.models import User
from boards_app.api.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                     write_only=True,
                                                     source="assignee",
                                                     required=False,
                                                     allow_null=True,)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                     source="reviewer",
                                                     required=False,
                                                     write_only=True, 
                                                     allow_null=True,)
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)

    #comments_count = serializers.IntegerField(source="comments.count", read_only=True) for counting comments
    class Meta():
        model = TaskModel
        fields = ["id","board","title","description","status","priority","assignee_id","reviewer_id","assignee","reviewer","due_date"]

