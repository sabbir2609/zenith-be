# myapp/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Check if the provided username is an email
        is_email = "@" in username

        # Authenticate based on username or email
        if is_email:
            user = UserModel.objects.filter(email=username).first()
        else:
            user = UserModel.objects.filter(username=username).first()

        if user and user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
