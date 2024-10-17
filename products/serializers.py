from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','user_email', 'name', 'price', 'description', 'category', 'stock_quantity', 'image_url', 'created_date']

    def get_user_email(self, obj):
         return obj.user.email

class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'user_email', 'product_name', 'quantity', 'order_date']

    def get_user_email(self, obj):
           return obj.user.email
    def get_product_name(self, obj):
        return obj.product.name