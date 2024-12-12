from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.auth.models import User
import jdatetime


class RohamModel(models.Model):
    # سایر فیلدهای مدل خود را اینجا اضافه کنید

    class Meta:
        permissions = [
            ("is_frontend_user", "Can access frontend without CSRF check"),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name



class ProductsModel(models.Model):
    name = models.CharField(max_length=20)
    descriptions = models.TextField(max_length=200)
    image = models.ImageField(upload_to='media/')
    price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    # فیلد stock را از اینجا بردارید چون حالا موجودی هر سایز در مدل ProductSize مدیریت می‌شود

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey('ProductsModel',on_delete=models.CASCADE ,related_name='product_images')
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

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password  # افزودن check_password

class RegisterModelManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)  # تنظیم رمز عبور
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)

class RegisterModel(AbstractBaseUser, PermissionsMixin):
    phone_validator = RegexValidator(regex=r'^09\d{9}$')

    name = models.CharField(max_length=50)  # الزامی
    lastname = models.CharField(max_length=50)  # الزامی
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = RegisterModelManager()
    address = models.CharField(max_length=255, default='')  # الزامی
    city = models.CharField(max_length=100, default='')

    USERNAME_FIELD = 'phone'  # فیلدی که به عنوان نام کاربری استفاده می‌شود
    REQUIRED_FIELDS = ['name', 'lastname']  # نام و نام خانوادگی الزامی هستند

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # فقط ذخیره‌سازی عادی، بدون هَش کردن

    def verify_password(self, raw_password):
        return raw_password == self.password  # تطابق رمز عبور ساده

    def __str__(self):
        return f"{self.name} {self.lastname} - {self.phone}"




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,default='')
    city = models.CharField(max_length=100,default='')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    @property
    def shamsi_created_at(self):
        # تبدیل تاریخ میلادی به تاریخ شمسی
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"Order {self.id} by {self.user.name} {self.user.lastname}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    size = models.CharField(max_length=2)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)