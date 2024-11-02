from django.contrib import admin
from .models import *


@admin.register(RegisterModel)
class RegisterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'phone')  # حذف password به دلایل امنیتی
    search_fields = ('name', 'lastname')
    ordering = ('name',)
    list_filter = ('lastname',)
    list_editable = ('phone',)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 4  # تعداد فیلدهای اضافی برای سایزها

class imageinline(admin.TabularInline):
    model = ProductImages
    extra=1


@admin.register(ProductsModel)
class ProductAdmin(admin.ModelAdmin):
    list_display =('name','descriptions','image')
    list_editable=('descriptions','image')

    inlines = [ProductSizeInline,imageinline]


# @admin.register(ProductSize)
# class ProductSizeAdmin(admin.ModelAdmin):
#     list_display = ('product','size','stock')
#     list_editable = ('size','stock')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','total_price','city','created_at','is_paid','address')
    list_editable = ('total_price','city','is_paid','address')


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order','product','size','quantity','price')
    

    