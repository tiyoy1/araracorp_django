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
        fields = ['id', 'menu_item_name', 'menu_item', 'quantity', 'unit_price', 'subtotal', 'note' ]
        extra_kwargs = {
            'unit_price' : {'required' : False}
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta: 
        model = Order
        fields = ['id', 'table', 'status', 'note', 'items', 'total', 'created_at', 'updated_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['table', 'note', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data :
            menu_item = item['menu_item']
            OrderItem.objects.create(
                order = order,
                menu_item = menu_item,
                quantity = item['quantity'],
                unit_price = menu_item.price,
                note = item.get('note', ''  )
            )
            return order
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'change' : {'required' : False}
        }

    def validate(self, data):
        order = data['order']
        amount_paid = data['amount_paid']
        order_total = order.total

        if amount_paid < order_total:
            raise serializers.ValidationError({
                'amount_paid' : f"Insufficient payment dude. Order total is {order_total}"
            })
        
        data['change'] = amount_paid - order_total
        return data