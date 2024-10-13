from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login , authenticate
from django.db import models
from .forms import *
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from .models import RegisterModel



def home(request):
    user = request.user
    return render(request,'home/home.html',{'user':user})



def product(request):
    pass



def loginView(request):
    form = LoginForm()  # تعریف متغیر form در ابتدا
    error = False  # متغیر error برای مدیریت خطاها

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            user = authenticate(request, username=phone, password=password)  # استفاده از authenticate
            if user is not None:
                login(request, user)
                messages.success(request, "به سیستم خوش آمدید!")
                return redirect('zebrashopapp:home')
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                error = True

    return render(request, 'login/login.html', {'form': form, 'error': error})



class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = RegisterModel.objects.get(phone=username)
        except RegisterModel.DoesNotExist:
            return None



def RegisterView(request):

    erorr=False
    
    form = RegisterForm()

    if request.method== "POST":
        erorr = False
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zebrashopapp:home')
        else:
            form = RegisterForm()
            erorr = True

    return render(request,'register/register.html', {'form':form ,'error':erorr})




def MenuViews(request):
    products = ProductsModel.objects.all()  # دریافت تمام محصولات
    context = {
        'products': products  # ارسال محصولات به قالب
    }
    
  
    return render(request, 'menu/menu.html', context)



def product_detail(request,id):
    product = get_object_or_404(ProductsModel, id=id)
    return render(request, 'product-detail/product-detail.html', {'product': product})




def basket_view(request, id):
    basket = request.session.get('basket', {})  # دریافت سبد خرید از session
    total_price = 0  # متغیر برای ذخیره مجموع قیمت

    # محاسبه مجموع قیمت محصولات در سبد خرید
    for item in basket.values():
        total_price += item['price'] * item['quantity']

    context = {
        'basket': basket,
        'total_price': total_price,
    }

    return render(request, 'basket/basket.html', context)  # صفحه‌ای برای نمایش سبد خرید




def add_to_basket(request,id):
    if request.method == 'POST':
        # دریافت اطلاعات محصول
        product = get_object_or_404(ProductsModel, id=id)

        # دریافت سایز انتخاب شده
        selected_size_id = request.POST.get('size')
        selected_size = get_object_or_404(ProductSize, id=selected_size_id)

        # دریافت سبد خرید از session
        basket = request.session.get('basket', {})

        # بررسی اینکه آیا محصول قبلاً به سبد خرید اضافه شده یا خیر
        if str(product.id) in basket:
            basket[str(product.id)]['quantity'] += 1  # افزایش تعداد محصول
        else:
            basket[str(product.id)] = {
                'name': product.name,
                'price': product.price,
                'size': selected_size.size,
                'quantity': 1
            }

        # به‌روزرسانی session
        request.session['basket'] = basket

        return redirect('zebrashopapp/product-detail.html',id=product.id)  # یا هر صفحه‌ای که می‌خواهید



class ProductImage(models.Model):
    product = models.ForeignKey(ProductsModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"
    

def ProfileViews(request):
    pass