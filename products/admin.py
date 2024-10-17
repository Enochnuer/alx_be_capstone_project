from django.contrib import admin
from django.contrib import admin
from .models import  Product, Order
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'image_url', 'created_date')
    search_fields = ('name', 'category')
    list_filter = ('name', 'category', 'price', 'stock_quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'order_date')
    search_fields = ('user__username', 'product__name')  # Enables search by username and product name
    list_filter = ('order_date', 'quantity', 'product__name')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)