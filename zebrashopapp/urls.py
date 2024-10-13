from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView #for loging out

app_name = 'zebrashopapp'

urlpatterns = [
    path('',views.home ,name='home'),
    path('login',views.loginView , name='login'),
    path('register',views.RegisterView,name='register'),
    path('menu',views.MenuViews,name='menu'),
    path('product-detail/<int:id>/',views.product_detail,name='product-detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile',views.ProfileViews , name='profile'),
    path('add-to-basket/<int:id>/', views.basket_view, name='add_to_basket'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)