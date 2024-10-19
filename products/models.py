from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Product(models.Model):
    ELECTRONICS = 'electronics'
    CLOTHING = 'clothing'
    ACCESSORIES = 'accessories'


    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (CLOTHING, 'Clothing'),
        (ACCESSORIES, 'Accessories'),
    ]
    name = models.CharField(max_length=250, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    description = models.TextField(max_length=1000)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=False
    )
    stock_quantity = models.PositiveIntegerField(blank=False)
    image_url = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def clean(self):
        super().clean()
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': 'Stock quantity cannot be negative.'})
        
    def reduce_stock(self, quantity):
        """Reduces stock quantity by the specified amount."""
        if quantity > self.stock_quantity:
            raise ValueError("Not enough stock to fulfill this order.")
        
        self.stock_quantity -= quantity
        self.save()
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  
    order_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        self.clean()  
        self.product.reduce_stock(self.quantity)  # Update stock
        super().save(*args, **kwargs)  
    def __str__(self):
        return f"Order of {self.quantity} {self.product.name} by {self.user.username}"