from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login , authenticate, get_backends
from django.db import models
from .forms import *
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail




def home(request):
    user = request.user
    return render(request,'home/home.html',{'user':user})



def product(request):
    pass



def loginView(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            user = RegisterModel.objects.get(phone=phone)
            if user.check_password(password):
                # ورود موفق
                # از request.user.set_authenticated استفاده کنید اگر نیاز دارید
                # با استفاده از session می‌توانید کاربر را در سیستم نگه دارید
                request.session['user_id'] = user.id  # ذخیره id کاربر در سشن
                return redirect('zebrashopapp:home')  # به صفحه اصلی یا هر صفحه دیگر بروید
            else:
                messages.error(request, 'رمز عبور نادرست است.')
        except RegisterModel.DoesNotExist:
            messages.error(request, 'کاربر وجود ندارد.')

    return render(request, 'login/login.html')



class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = RegisterModel.objects.get(phone=username)
        except RegisterModel.DoesNotExist:
            return None



from django.contrib.auth import login

def RegisterView(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.save()


             # دریافت بک‌اند احراز هویت مورد استفاده
            backend = get_backends()[0]  # انتخاب اولین بک‌اند یا بک‌اند مورد نظر
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            # لاگین کاربر بعد از ثبت‌نام
            login(request, user)

            return redirect('zebrashopapp:home')

    return render(request, 'register/register.html', {'form': form})




def MenuViews(request):
    products = ProductsModel.objects.all()
    images = ProductImages.objects.all()  
    context = {
        'products': products,
        'images': images  
    }
    
  
    return render(request, 'menu/menu.html', context)



def product_detail(request,id):
    product = get_object_or_404(ProductsModel, id=id)
    sizes = product.sizes.all()
    return render(request, 'product-detail/product-detail.html', {'product': product ,'sizes':sizes})




def basket_view(request):
    # بازیابی سبد خرید از جلسه
    basket = request.session.get('basket', {})
    total_price = 0

    # محاسبه قیمت کل
    for item in basket.values():
        total_price += item['price'] * item['quantity']

    context = {
        'basket': basket,
        'total_price': total_price
    }

    return render(request, 'basket/basket.html', context)


def add_to_basket(request, id):
    if request.method == 'POST':
        product = get_object_or_404(ProductsModel, id=id)
        selected_size_id = request.POST.get('size')
        selected_size = get_object_or_404(ProductSize, id=selected_size_id)

        # بازیابی سبد خرید از جلسه
        basket = request.session.get('basket', {})

        # بررسی اینکه آیا محصول در سبد خرید وجود دارد
        if str(product.id) in basket:
            basket[str(product.id)]['quantity'] += 1
        else:
            # اضافه کردن محصول به سبد خرید
            basket[str(product.id)] = {
                'name': product.name,
                'price': product.price,
                'size': selected_size.size,
                'quantity': 1
            }

        # ذخیره سبد خرید در جلسه
        request.session['basket'] = basket
        return redirect('zebrashopapp:product-detail', id=product.id)

    return redirect('zebrashopapp:product-detail', id=id)


def remove_from_basket(request, item_id):
    if request.method == 'POST':
        # بازیابی سبد خرید از جلسه
        basket = request.session.get('basket', {})

        # بررسی وجود آیتم در سبد
        if item_id in basket:
            del basket[item_id]
            request.session['basket'] = basket

    return redirect('zebrashopapp:basket_view')


    

@login_required
def ProfileViews(request):
    user = request.user  # کاربر فعلی
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user.address = form.cleaned_data['address']  # فقط آدرس را بروزرسانی کن
            user.save()  # ذخیره تغییرات
            return redirect('zebrashopapp:profile')  # به صفحه پروفایل بازگشت
    else:
        form = ProfileForm(instance=user)  # فرم را با اطلاعات کاربر پر کن
    
    return render(request, 'profile/profile.html', {'form': form, 'user': user})




def calculate_total_price(order_items):
    total_price = sum(item.price * item.quantity for item in order_items)
    return total_price

def checkout(request):
    # فرض می‌کنیم که کاربر فعلی را می‌توانیم به دست آوریم
    order_items = OrderItem.objects.filter(order__user=request.user)  # فیلتر بر اساس کاربر فعلی
    total_price = calculate_total_price(order_items)

    if request.method == 'POST':
        form = OrderReviewForm(request.POST)  # دریافت داده‌های فرم
        if form.is_valid():
            # ساخت یک شی جدید از مدل Order
            order = Order(
                user=request.user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                total_price=total_price,
            )
            order.save()  # ذخیره سفارش
            # اینجا می‌توانید منطق مربوط به پرداخت را اضافه کنید
            return redirect('payment_success')  # مسیر موفقیت پرداخت (تعریف کن)

    else:
        # در صورت GET، فرم جدید را ایجاد کن
        form = OrderReviewForm(initial={
            'address': request.user.address or '',  # اطمینان از خالی نبودن
            'city': request.user.city or '',
        })

    context = {
        'form': form,
        'total_price': total_price,
        'order_items': order_items,  # اضافه کردن order_items به context برای نمایش
    }
    return render(request, 'checkout.html', context)