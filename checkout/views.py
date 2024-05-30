# checkout/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Payment, Cart, CartItem
from products.models import Products
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = Products.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, status='open')
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    cart_item.save()
    
    cart_quantity = sum(item.quantity for item in cart.cartitem_set.all())
    cart_subtotal = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    
    return JsonResponse({
        'cart_quantity': cart_quantity,
        'cart_subtotal': cart_subtotal,
    })

def checkout(request):
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=calculate_cart_total(request))
        for item in get_cart_items(request):
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['price'])

        Payment.objects.create(order=order, amount=order.total, payment_method='Credit Card', status='Completed')
        clear_cart(request)

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_id=order.id)

    context = {
        'cart_items': get_cart_items(request),
        'total': calculate_cart_total(request)
    }
    return render(request, 'checkout/checkout.html', context)

def calculate_cart_total(request):
    cart, created = Cart.objects.get_or_create(user=request.user, status='open')
    return sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

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
    
def cart_contents(request):
    cart, created = Cart.objects.get_or_create(user=request.user, status='open')
    cart_items = CartItem.objects.filter(cart=cart)
    
    items = [
        {
            'product_name': item.product.name,
            'product_price': item.product.price,
            'quantity': item.quantity
        }
        for item in cart_items
    ]
    
    cart_subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
    return JsonResponse({
        'cart_items': items,
        'cart_subtotal': cart_subtotal,
    })