from rest_framework import serializers
from comments_app.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.first_name')

    class Meta:
        model = Comment
        fields = ['id','created_at','author','content']
        read_only_fields = ['task','author']