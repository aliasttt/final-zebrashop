from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

    
class ProductsModel(models.Model):
    name = models.CharField(max_length=20)
    descriptions = models.TextField(max_length=200)
    image = models.ImageField(upload_to='media/')
    price = models.IntegerField(default=0)
    # فیلد stock را از اینجا بردارید چون حالا موجودی هر سایز در مدل ProductSize مدیریت می‌شود

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey('ProductsModel',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/products')

    def __str__(self):
        return self.product.name


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('S', 'S'),  
        ('M', 'M'),  
        ('L', 'L'),   
        ('XL', 'XL')  
    ]
    
    product = models.ForeignKey('ProductsModel', on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)  # موجودی برای هر سایز

    def __str__(self):
        return f"{self.product.name} - {self.size}"

class RegisterModel(models.Model):

    phone_validator = RegexValidator(regex=r'^09\d{9}$')

    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=11 ,unique=True,validators=[phone_validator])
    last_login = models.DateTimeField(auto_now=True)
    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = make_password(self.password)  # هش کردن رمز عبور
    #     super().save(*args, **kwargs)