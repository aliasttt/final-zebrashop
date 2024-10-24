from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from zebrashopapp.models import RegisterModel

class AuthTestCase(TestCase):
    def setUp(self):
        self.user = RegisterModel.objects.create(
            phone='09385101617',
            name='ali',
            lastname='asadi',
            password='Aasadi2233#'
        )

    def testLogin(self):
        # تست ورود به سیستم
        login_success = auth.authenticate(username='09385101617', password='Aasadi2233#')
        self.assertIsNotNone(login_success)  # کاربر باید پیدا شده باشد

        if login_success:
            print(f"کاربر پیدا شد: {login_success.name} {login_success.lastname} - {login_success.phone}")
        else:
            print("کاربر پیدا نشد.")