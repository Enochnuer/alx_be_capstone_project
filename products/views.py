from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework as django_filters
from .models import Product
from .serializers import ProductSerializer
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# Create your views here.
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Partial match
    category = django_filters.ChoiceFilter(field_name='category', lookup_expr='icontains')
    price = django_filters.RangeFilter(field_name='price')  # For price range filtering
    stock_quantity = django_filters.NumberFilter(field_name='stock_quantity', lookup_expr='gte')  # Available stock

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock_quantity']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter, django_filters.DjangoFilterBackend)
    filterset_class = ProductFilter
    ordering_fields = ['price', 'created_date']  # Allow ordering by price or created date
    ordering = ['created_date']  # Default ordering
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Additional filtering by stock availability (optional)
        if self.request.query_params.get('in_stock') is not None:
            in_stock = self.request.query_params.get('in_stock') == 'true'
            if in_stock:
                queryset = queryset.filter(stock_quantity__gt=0)

        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  #  Require authentication for order actions

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

    def get_queryset(self):
        return Order.objects.all().order_by('order_date') 
