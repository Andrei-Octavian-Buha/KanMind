from rest_framework import serializers
from comments_app.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for task comments.

    Handles:
    - displaying comment content
    - exposing author name (read-only)
    - creation timestamp
    """
    author = serializers.ReadOnlyField(source='author.first_name')

    class Meta:
        model = Comment
        fields = ['id','created_at','author','content']
        read_only_fields = ['task','author']