from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest


class EmailAuthBackend(BaseBackend):
    # авторизация по email
    def authenticate(self, request: HttpRequest, username=None, password=None, **kwargs):
        UserModel = get_user_model()  # модель user
        try:
            # вместо username поступает пароль
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        #
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int):
        UserModel = get_user_model()  # модель user
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

