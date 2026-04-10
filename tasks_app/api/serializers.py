from rest_framework import serializers
from tasks_app.models import TaskModel
from django.contrib.auth.models import User
from auth_app.api.serializers import UserSerializer
from boards_app.models import BoardsModel

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for TaskModel.

    Handles:
    - Task creation and update
    - Nested read-only representation for assignee/reviewer
    - Foreign key assignment via *_id fields
    - Aggregated comment count
    """
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                     write_only=True,
                                                     source="assignee",
                                                     required=False,
                                                    )
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                     source="reviewer",
                                                     required=False,
                                                     write_only=True,
                                                    )
    board = serializers.PrimaryKeyRelatedField(queryset=BoardsModel.objects.all())
    
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    class Meta():
        model = TaskModel
        fields = ["id","board","title","description","status",
                  "priority","assignee_id","reviewer_id","assignee",
                  "reviewer","due_date", "comments_count"
        ]

    def get_comments_count(self,obj):
        """
        Returns total number of comments attached to the task.
        """
        return obj.comments.count()
    
    def validate(self, data):
        board = data.get('board')
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError(
                {"assignee_id": "The user should be member"}
            )
        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError(
                {"reviewer_id": "Reviewer should be member "}
            )
        return data