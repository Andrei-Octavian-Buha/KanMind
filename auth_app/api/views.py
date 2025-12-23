from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate


class UserPorfileList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response(
                {"detail":"Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate( 
            username=user.username,
            password=password
        )
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "fullname": user.username,
            "email": user.email,
            "user_id": user.id
        })

class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail":"Logout succesed"}, status=status.HTTP_200_OK)

