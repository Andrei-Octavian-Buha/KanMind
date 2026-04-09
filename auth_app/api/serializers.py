from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning public user data.
    Used mainly for profile display / API responses.
    """

    fullname = serializers.CharField(source="first_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer responsible for user registration.

    Handles:
    - password confirmation validation
    - email uniqueness check
    - user creation with token generation
    """
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(source="first_name", write_only=True)

    class Meta:
        model = User
        fields = ["id", "fullname", "email", "password", "repeated_password"]

    def validate(self, data):
        """
        Ensure password and repeated_password match.
        """
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({"Password": "Passwords do not match"})
        return data

    def validate_email(self, value):
        """
        Ensure email is unique in the system.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        """
        Create a new user instance.

        Uses email as username and hashes password automatically.
        Also creates an auth token.
        """
        first_name = validated_data.get("first_name", "")
        validated_data.pop("repeated_password")

        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=first_name,
        )
        Token.objects.create(user=user)

        return user


class EmailAuthSerializer(serializers.Serializer):
    """
    Authentication serializer using email + password.

    Validates credentials using Django authenticate system
    and attaches the user object if valid.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, atters):
        """
        Validate login credentials.

        Returns user object if authentication succeeds.
        """
        email = atters.get("email")
        password = atters.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Login data dont match", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                "You need to add email and password", code="authorization"
            )

        atters["user"] = user
        return atters

