from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User
from .serializers import RegisterSerializer, EmailAuthSerializer
from boards_app.api.serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterView(APIView):
    """
    API endpoint for user registration.

    Creates a new user account and returns an authentication token
    along with basic user information.

    Permissions:
        - Public (AllowAny)
    """
        
    permission_classes = [AllowAny]

    """
    Handle user registration.

    Request body:
        email (str): User email
        password (str): User password
        first_name (str): User first name

    Returns:
        201: User successfully created with token
        400: Validation errors
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.first_name,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(ObtainAuthToken):
    """
    API endpoint for user authentication.

    Authenticates a user using email and password and returns
    an authentication token with user details.

    Permissions:
        - Public (AllowAny)
    """
    serializer_class = EmailAuthSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        """
        Handle user login.

        Request body:
            email (str): User email
            password (str): User password

        Returns:
            200: Token and user data
            400: Invalid credentials
        """
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "fullname": user.first_name,
                "email": user.email,
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CheckEmailView(APIView):
    """
    API endpoint to check if a user exists by email.

    Requires authentication.

    Permissions:
        - Authenticated users only
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        """
        Retrieve user information by email.

        Query params:
            email (str): Email to search for

        Returns:
            200: User data
            400: Missing email parameter
            404: User not found
        """
        email = request.query_params.get('email')

        if not email:
            return Response(
                {'email':'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error':'Email not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

        

class LogoutView(APIView):
    """
    API endpoint for user logout.

    Deletes the current user's authentication token.

    Permissions:
        - Authenticated users only
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Invalidate the user's token.

        Returns:
            200: Logout successful
        """
        request.user.auth_token.delete()
        return Response({"detail":"Logout succeeded"}, status=status.HTTP_200_OK)

