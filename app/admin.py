from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Order, Cart, Product

class CustomerAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'address', 'contact_no']

# Rest of your admin classes remain the same


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'product_price', 'product_image']

class CartAdmin(admin.ModelAdmin):
    list_display=['user', 'product_id' , 'quantity']

# Register your models with the appropriate admin classes
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)
admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)
