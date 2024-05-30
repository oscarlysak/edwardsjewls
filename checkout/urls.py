# checkout/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_product_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_user_cart'),
    path('cart/contents/', views.cart_contents, name='cart_contents'),
    path('checkout/', views.checkout, name='checkout'),
]