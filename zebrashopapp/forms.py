from.models import *
from django import forms

class RegisterForm(forms.ModelForm):
    password =forms.CharField(widget = forms.PasswordInput)

    class Meta :
        model = RegisterModel
        fields = ['name','lastname','password','phone']


class LoginForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
    )
    password = forms.CharField()



class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductsModel
        fields = ['name', 'descriptions', 'image']