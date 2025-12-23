from rest_framework import serializers
from tasks_app.models import Task
from django.contrib.auth.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username')
    
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    owner = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assigned', 'reviewer', 'due_date', 'comments_count','owner'
        ]

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned', [])
        task = Task.objects.create(**validated_data)
        task.assigned.set(assigned_users)
        return task