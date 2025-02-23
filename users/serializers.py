from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "username", "email", "password", "role", "avater")