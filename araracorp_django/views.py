from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from araracorp_django.models import Category, MenuItem, Table, Order, Payment
from araracorp_django.serializers import *

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemListView(generics.ListCreateAPIView):
    queryset =  MenuItem.objects.filter(is_available = True)
    serializer_class = MenuItemSerializer

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class TableListView(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = CategorySerializer

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST' :
            return CreateOrderSerializer
        return OrderSerializer

class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderStatusUpdateView(APIView):
    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        new_status = request.data.get('status')
        order.status = new_status
        order.save()
        return Response({'status' : order.status})
    
class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
        