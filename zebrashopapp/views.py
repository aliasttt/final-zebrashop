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
from django.views.decorators.csrf import csrf_exempt


@login_required
def custom_view(request):
    # بررسی کنید که آیا کاربر دارای permission خاصی هست یا خیر
    if request.user.has_perm('zebrashopapp.is_frontend_user'):
        # معاف کردن کاربر از بررسی CSRF
        return process_without_csrf(request)
    else:
        # سایر کاربران با توکن CSRF بررسی می‌شوند
        return process_with_csrf(request)

@csrf_exempt
def process_without_csrf(request):
    # پردازش درخواست برای کاربرانی که از بررسی CSRF معاف هستند
    return JsonResponse({'message': 'CSRF check skipped for frontend user'})

def process_with_csrf(request):
    # پردازش درخواست برای سایر کاربران
    return JsonResponse({'message': 'CSRF check completed'})




def home(request):
    user = request.user
    return render(request,'home/home.html',{'user':user})



def product(request):
    pass


@csrf_exempt
def loginView(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(request, username=phone, password=password)  # authenticate با استفاده از شماره تلفن و پسورد

        if user is not None:
            login(request, user)  # لاگین کاربر
            return redirect('zebrashopapp:home')
        else:
            messages.error(request, 'شماره تلفن یا رمز عبور نادرست است.')

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
        
        # ثبت سفارش و آیتم سفارش در مدل
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(
                user=request.user,
                is_paid=False  # فقط سبد خرید غیر پرداخت شده
            )
            order_item, item_created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                size=selected_size.size,
                defaults={'quantity': 0, 'price': product.price}
            )

            # افزایش تعداد آیتم در سفارش
            order_item.quantity += 1
            order_item.save()

            # محاسبه مجموع قیمت و مقداردهی به total_price
            order.total_price = sum(item.price * item.quantity for item in order.items.all())  # استفاده از related_name
            order.save()  # ذخیره‌سازی تغییرات در مجموع قیمت

        return redirect('zebrashopapp:product-detail', id=product.id)

    return redirect('zebrashopapp:product-detail', id=id)


from django.http import JsonResponse

from django.shortcuts import redirect, get_object_or_404
from .models import OrderItem

def remove_from_basket(request, item_id):
    if request.method == "POST":
        try:
            # حذف از سبد خرید در سشن
            basket = request.session.get('basket', {})
            if item_id in basket:
                del basket[item_id]  # حذف آیتم از سبد خرید در سشن
                request.session['basket'] = basket
                
                # اگر سبد خرید خالی شد، سبد را از سشن حذف کنید
                if not basket:
                    del request.session['basket']

            # حذف آیتم از دیتابیس
            order_item = get_object_or_404(OrderItem, id=item_id)  # با فیلتر کاربر اگر لازم است
            order_item.delete()  # حذف آیتم از دیتابیس

            return redirect('zebrashopapp:basket_view')  # ریدایرکت به ویوی سبد خرید
            
        except Exception as e:
            return redirect('zebrashopapp:basket_view')  # در صورت بروز خطا نیز ریدایرکت کنید
    else:
        return redirect('zebrashopapp:basket_view')

def checkout_view(request):
    # تابع برای نمایش صفحه پرداخت
    order_items = []  # لیست آیتم‌های سفارش (باید از سبد خرید استخراج شود)
    total_price = 0  # مجموع قیمت

    # کدهای لازم برای پر کردن order_items و total_price

    context = {
        'order_items': order_items,
        'total_price': total_price,
        'user_info': request.user,  # فرض بر این است که اطلاعات کاربر وجود دارد
    }
    return render(request, 'your_template.html', context)



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
    order_items = OrderItem.objects.filter(order__user=request.user, order__is_paid=False)  # آیتم‌های سبد خرید کاربر

    if not order_items.exists():
        # اگر آیتمی در سبد خرید نیست، هدایت به صفحه سبد خرید
        return redirect('zebrashopapp:basket_view')

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
                is_paid=False,  # در ابتدا پرداخت نشده است
            )
            order.save()  # ذخیره سفارش

            # به‌روزرسانی آیتم‌های سبد خرید به سفارش جدید
            order_items.update(order=order)  # حذف status='ordered' چون فیلد status در مدل OrderItem وجود ندارد

            # پاک کردن سبد خرید از سشن
            if 'basket' in request.session:
                del request.session['basket']

            # اینجا می‌توانید منطق مربوط به پرداخت را اضافه کنید

            return redirect('zebrashopapp:checkout_success')  # مسیر موفقیت پرداخت (تعریف کن)
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
    return render(request, 'checkout/checkout.html', context)



def previous_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
    else:
        orders = []

    return render(request, 'previous_orders/previous_orders.html', {'orders': orders})




def About_Us(request):
    return render(request,'about_us/about_us.html')


def Contact_Us(request):
    context = {}  # ایجاد کانتکست برای ارسال پیام‌ها به قالب

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')  # ایمیل کاربر
        message = request.POST.get('message')

        # متن ایمیل
        email_subject = f"پیام از طرف {name}"
        email_message = f"نام و نام خانوادگی: {name}\nشماره تماس: {phone}\nایمیل: {email}\n\nپیام:\n{message}"

        # تلاش برای ارسال ایمیل
        try:
            send_mail(
                email_subject,
                email_message,
                "aliasadi3853@gmail.com",  # ایمیل شما به عنوان فرستنده
                ["aliasadi3853@gmail.com"],  # ایمیل شما به عنوان گیرنده
                fail_silently=False,
            )
            context['success_message'] = 'پیام شما با موفقیت ارسال شد!'
        except Exception as e:
            context['error_message'] = f"خطا در ارسال ایمیل: {e}"

    return render(request, 'contact_us/contact_us.html', context)