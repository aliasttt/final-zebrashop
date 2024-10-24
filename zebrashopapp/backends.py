from django.contrib.auth.backends import ModelBackend
from .models import RegisterModel
from django.contrib.auth.hashers import check_password

class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = RegisterModel.objects.get(phone=username)
        except RegisterModel.DoesNotExist:
            return None

        # بررسی رمز عبور به صورت متن ساده
        if password == user.password:
            return user
        return None

    def get_user(self, user_id):
        try:
            return RegisterModel.objects.get(pk=user_id)
        except RegisterModel.DoesNotExist:
            return None