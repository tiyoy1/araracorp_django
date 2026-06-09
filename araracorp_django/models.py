from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    category = models.ForeignKey(Category,  on_delete=models.SET_NULL, null=True, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image= models.ImageField(upload_to="menu/", blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def subtotal(self):
        return self.quantity * self.unit_price
    
class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('qris', 'QRIS'),
        ('transfer', 'Bank Transfer'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
