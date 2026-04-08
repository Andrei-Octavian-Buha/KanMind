from rest_framework import serializers
from boards_app.models import BoardsModel
from django.contrib.auth.models import User 
from auth_app.api.serializers import UserSerializer




class BoardsSerializer(serializers.ModelSerializer):
    """
    Serializer for board list and create/update operations.

    Handles:
    - basic board data
    - assigning members
    - computed statistics (tasks, priority counts)
    """
    members = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        many=True,
        write_only=True)
    members_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id',read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BoardsModel
        fields = ['id','title','members','members_count','ticket_count','tasks_to_do_count','tasks_high_prio_count','owner_id']
    
    def get_members_count(self, obj):
        """
        Returns number of members in a board.
        """
        return obj.members.count()
    
    def update(self, instance, validated_data):
        """
        Updates board data and optionally replaces members list.
        """
        members = validated_data.pop('members',None)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        if members is not None:
            instance.members.set(members)
        return instance
    
    def create(self, validated_data):
        """
        Creates a board and assigns members if provided.
        """
        members = validated_data.pop('members',[])
        board = BoardsModel.objects.create(**validated_data)
        board.members.set(members)
        return board
    
class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single board view.

    Includes:
    - full member data
    - related tasks
    """
    tasks = serializers.SerializerMethodField()
    members = UserSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source='owner.id',read_only=True)

    class Meta:
        model = BoardsModel
        fields = ['id','title','owner_id','members','tasks']

    def get_tasks(self, obj):
        """
        Returns all tasks related to this board.
        """
        from tasks_app.api.serializers import TaskSerializer
        return TaskSerializer(obj.taskmodel_set.all(), many=True).data
    

class BoardPatchSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer used for partial updates.

    Provides read-only structured representation of:
    - owner
    - members
    """
    owner_data = UserSerializer(source='owner',read_only=True)
    members_data = UserSerializer(source='members',many=True,read_only=True)

    class Meta:
        model = BoardsModel
        fields = ['id','title','owner_data','members_data']