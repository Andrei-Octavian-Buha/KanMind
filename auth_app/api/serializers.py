from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(source='first_name', write_only=True)
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
        first_name = validated_data.get('first_name', '')
        validated_data.pop('repeated_password')

        user = User.objects.create_user(
            username =validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
        )
        Token.objects.create(user=user)

        return user
    

class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'}, trim_whitespace=False)

    def validate(self,atters):
        email = atters.get('email')
        password = atters.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email,password=password)
            if not user:
                raise serializers.ValidationError('Login data dont match', code='authorization')
        else:
            raise serializers.ValidationError('You need to add email and password',code='authorization')
        
        atters['user'] = user
        return atters