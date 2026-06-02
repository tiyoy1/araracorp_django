from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('menu/', views.MenuItemListView.as_view()),
    path('menu/<int:pk>/', views.MenuItemDetailView.as_view()),
    path('tables/', views.TableListView.as_view()),
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailView.as_view()),
    path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view()),
    path('payments/', views.PaymentCreateView.as_view()),
]