from rest_framework import serializers
from .models import Category, MenuItem, Table, Order, OrderItem, Payment

class CategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model= MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available', 'category_name']

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only= True) 
    subtotal = serializers.DecimalField(max_digits=8, decimal_places=2, read_only= True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menut_item_name', 'menu_item', 'quantity', 'unit_price', 'subtotal', 'note' ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
