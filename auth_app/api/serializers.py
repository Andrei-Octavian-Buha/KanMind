from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserProfileSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["token","id","email","username"]
    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(source='username')
    class Meta:
        model =  User
        fields = ['id','fullname','email','password','repeated_password']
    
    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"Password":"Passwords do not match"})
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    
    def create(self, validated_data):
        validated_data.pop('repeated_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)

        return user
