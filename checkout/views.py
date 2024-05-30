# checkout/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Order, OrderItem, Payment, Cart, CartItem
from products.models import Products
from django.contrib import messages
from django.utils.crypto import get_random_string


def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key, status='open')
    return cart

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Products, id=product_id)
    cart = get_cart(request)
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

def cart_contents(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    items = [
        {
            'product_name': item.product.name,
            'product_price': item.product.price,
            'quantity': item.quantity,
            'product_image': item.product.images.first().image.url if item.product.images.first() else 'https://d3e54v103j8qbb.cloudfront.net/plugins/Basic/assets/placeholder.60f9b1840c.svg'
        }
        for item in cart_items
    ]
    
    cart_subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
    return JsonResponse({
        'cart_items': items,
        'cart_subtotal': cart_subtotal,
    })


def calculate_cart_total(cart):
    return sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

def get_cart_items(cart):
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

def clear_cart(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.delete()
    cart.status = 'closed'
    cart.save()


def remove_product_from_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart_contents')

def view_cart(request):
    cart = get_cart(request)
    items = get_cart_items(cart)
    return render(request, 'checkout/cart.html', {'items': items})

def checkout(request):
    if request.method == 'POST':
        cart = get_cart(request)
        order = Order.objects.create(session_key=cart.session_key, total=calculate_cart_total(cart))
        for item in get_cart_items(cart):
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['price'])

        Payment.objects.create(order=order, amount=order.total, payment_method='Credit Card', status='Completed')
        clear_cart(cart)

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_id=order.id)

    cart = get_cart(request)
    context = {
        'cart_items': get_cart_items(cart),
        'total': calculate_cart_total(cart)
    }
    return render(request, 'checkout/checkout.html', context)