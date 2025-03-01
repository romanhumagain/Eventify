from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.db import transaction
from .models import User
from .serializers import LoginSerializer, UserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os

# for handling user login
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Check if the user exists and authenticate
            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"error": "User with this email does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                # Generate refresh and access tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    "detail": "User logged in successfully.",
                    "refresh_token": str(refresh),
                    "access_token": access_token,
                    "is_organizer": user.is_organizer,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            return Response(
                {"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for handling user registration
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            # Handle user creation within a transaction to ensure rollback on error
            with transaction.atomic():
                user = serializer.save()

                # Generate the refresh and access tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    "detail": "User registered successfully.",
                    "refresh_token": str(refresh),
                    "access_token": access_token,
                    "is_organizer": user.is_organizer,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# For handling profile retrive, update and deletion
class UserRetriveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # For handling profile picture upload
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        
        # Check if a new profile picture is being uploaded
        if 'profile_picture' in request.FILES:
            # Delete old profile picture
            if user.profile_picture:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

        serializer = self.get_serializer(user, data=data, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handle deleting the user profile (soft delete)
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {"detail": "User profile deleted successfully."},
            status=status.HTTP_200_OK,
        )
