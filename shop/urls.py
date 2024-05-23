from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('filter_products', views.filter_products, name='filter_products')

]
