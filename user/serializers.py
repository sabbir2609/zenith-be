# user/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
