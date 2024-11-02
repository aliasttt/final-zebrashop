from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView #for loging out

app_name = 'zebrashopapp'

urlpatterns = [
    path('',views.home ,name='home'),
     path('login/', views.loginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('menu',views.MenuViews,name='menu'),
    path('product-detail/<int:id>/',views.product_detail,name='product-detail'),
    path('logout/', LogoutView.as_view(next_page='zebrashopapp:home'), name='logout'),
    path('profile',views.ProfileViews , name='profile'),
    path('add-to-basket/<int:id>/', views.add_to_basket, name='add_to_basket'),
    path('basket', views.basket_view, name='basket_view'),
    path('remove/<str:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success',views.checkout , name='checkout_success'),
    path('previous_orders',views.previous_orders , name='previous_orders'),
    path('custom-view/', views.custom_view, name='custom_view'),
    path('about_us',views.About_Us , name='about_us'),
    path('contact_us',views.Contact_Us , name='contact_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)