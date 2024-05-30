# checkout/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import Products

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=(
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ), default='Pending')
    total = models.FloatField()

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=(
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ), default='Pending')

    def __str__(self):
        return f"Payment for order {self.order.id}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('open', 'Open'), ('closed', 'Closed')), default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"
    
    def get_cart_items(request):
        cart, created = Cart.objects.get_or_create(user=request.user, status='open')
        cart_items = CartItem.objects.filter(cart=cart)
        items = [
            {
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price
            }
            for item in cart_items
        ]
        return items
    
    def clear_cart(request):
        cart = Cart.objects.get(user=request.user, status='open')
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item.delete()
        cart.status = 'closed'
        cart.save()