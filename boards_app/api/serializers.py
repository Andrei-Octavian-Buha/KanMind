from rest_framework import serializers
from boards_app.models import BoardsModel
from django.contrib.auth.models import User 
from auth_app.api.serializers import UserSerializer




class BoardsSerializer(serializers.ModelSerializer):
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
        return obj.members.count()
    
    def update(self, instance, validated_data):
        members = validated_data.pop('members',None)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        if members is not None:
            instance.members.set(members)
        return instance
    
    def create(self, validated_data):
        members = validated_data.pop('members',[])
        board = BoardsModel.objects.create(**validated_data)
        board.members.set(members)
        return board
    
class BoardDetailSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    members = UserSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source='owner.id',read_only=True)

    class Meta:
        model = BoardsModel
        fields = ['id','title','owner_id','members','tasks']

    def get_tasks(self, obj):
        from tasks_app.api.serializers import TaskSerializer
        return TaskSerializer(obj.taskmodel_set.all(), many=True).data
    
class BoardPatchSerializer(serializers.ModelSerializer):
    owner_data = UserSerializer(source='owner',read_only=True)
    members_data = UserSerializer(source='members',many=True,read_only=True)

    class Meta:
        model = BoardsModel
        fields = ['id','title','owner_data','members_data']