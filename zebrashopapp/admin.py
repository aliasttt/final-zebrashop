from django.contrib import admin
from .models import *

@admin.register(RegisterModel)
class RegisterMOdelAdmin(admin.ModelAdmin):
    list_display =('name','lastname','password','phone')
    search_fields = ('name', 'lastname') 
    ordering = ('name',)
    list_filter = ('lastname',)
    list_editable=('password','phone')


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
    
