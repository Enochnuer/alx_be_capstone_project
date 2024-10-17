from django.test import TestCase
from django.test import TestCase
from users.models import User
from .models import Product, Order
from django.core.exceptions import ValidationError
# Create your tests here.

class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@gmail.com')

    def test_create_product(self):
        product = Product.objects.create(
            name='Test Product',
            price=100.00,
            description='A test product description',
            category=Product.ELECTRONICS,
            stock_quantity=50,
            image_url='http://example.com/image.png',
            user=self.user
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.stock_quantity, 50)

    def test_stock_quantity_cannot_be_negative(self):
        product = Product(
            name='Test Product',
            price=100.00,
            description='A test product description',
            category=Product.ELECTRONICS,
            stock_quantity=-10,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            product.clean()

    def test_reduce_stock(self):
        product = Product.objects.create(
            name='Test Product',
            price=100.00,
            description='A test product description',
            category=Product.ELECTRONICS,
            stock_quantity=50,
            user=self.user
        )
        product.reduce_stock(10)
        self.assertEqual(product.stock_quantity, 40)

    def test_reduce_stock_not_enough_stock(self):
        product = Product.objects.create(
            name='Test Product',
            price=100.00,
            description='A test product description',
            category=Product.ELECTRONICS,
            stock_quantity=5,
            user=self.user
        )
        with self.assertRaises(ValueError):
            product.reduce_stock(10)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@gmail.com')
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            description='A test product description',
            category=Product.ELECTRONICS,
            stock_quantity=50,
            image_url='http://example.com/image.png',
            user=self.user
        )

    def test_create_order_and_reduce_stock(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=5
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 45)
        self.assertEqual(order.quantity, 5)

