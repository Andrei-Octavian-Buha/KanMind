from rest_framework import serializers
from boards_app.models import BoardsModel
from django.contrib.auth.models import User 


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='first_name', read_only=True)
    class Meta:
        model = User
        fields = ['id','email','fullname']

class BoardsSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        many=True,
        write_only=True)
    members_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id',read_only=True)

    class Meta:
        model = BoardsModel
        fields = ['id','title','members','members_count','owner_id']
    
    def get_members_count(self, obj):
        return obj.members.count()
    
    def create(self, validated_data):
        members = validated_data.pop('members',[])
        board = BoardsModel.objects.create(**validated_data)
        board.members.set(members)
        return board
    
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source='owner.id')

    class Meta:
        model = BoardsModel
        fields = ['id','title','owner_id','members']