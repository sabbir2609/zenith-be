# user/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from .serializers import (
    UsersSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    search_fields = ("username", "email")

    def get_serializer_class(self):
        if self.action == "profile" and self.request.method == "PUT":
            return UserSerializer
        elif self.action == "login":
            return UserLoginSerializer
        elif self.action == "logout":
            return UsersSerializer
        elif self.action == "get_user_by_id":
            return UserSerializer
        elif self.action == "register":
            return UserRegistrationSerializer
        else:
            return super().get_serializer_class()

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def get_user_by_id(self, request, pk=None):
        try:
            user = get_user_model().objects.get(pk=pk)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get", "put"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        if request.method == "PUT":
            serializer = self.get_serializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "post"], permission_classes=[AllowAny])
    def register(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "You are already logged in."}, status=status.HTTP_200_OK
            )

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "You are already logged in."},
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                login_response_serializer = self.get_serializer(user)
                return Response(
                    login_response_serializer.data, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        if request.user.is_authenticated:
            request.auth.delete()
            return Response(
                {"message": "Logged out successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "You are not logged in!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
