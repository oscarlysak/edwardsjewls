# shop/views.py
from django.shortcuts import render
from products.models import ProductCategory, Products, ProductImage, ProductStyle, ProductCondition
from django.http import JsonResponse
from django.db.models import Q

def shop(request):
    search_query = request.GET.get('q', '')
    
    filters = Q()
    if search_query:
        filters |= Q(name__icontains=search_query) | Q(description__icontains=search_query)
        filters |= Q(product_category__name__icontains=search_query) | Q(product_style__name__icontains=search_query)

    products = Products.objects.filter(filters)
    categories = ProductCategory.objects.all()
    styles = ProductStyle.objects.all()
    images = ProductImage.objects.all()
    
    return render(request, 'shop/shop.html', {'products': products, 'categories': categories, 'styles': styles, 'images': images})

def filter_products(request):
    category_id = request.GET.get('category_id')
    style_id = request.GET.get('style_id')
    search_query = request.GET.get('q', '')

    filters = Q()
    if category_id:
        filters &= Q(product_category_id=category_id)
    if style_id:
        filters &= Q(product_style_id=style_id)
    if search_query:
        filters &= Q(name__icontains=search_query) | Q(description__icontains=search_query)
        filters |= Q(product_category__name__icontains=search_query) | Q(product_style__name__icontains=search_query)

    products = Products.objects.filter(filters)

    product_list = []
    for product in products:
        first_image = product.images.first()
        product_list.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'SKU': product.SKU,
            'image_url': first_image.image.url if first_image else '/static/images/placeholder.svg'
        })

    return JsonResponse({'products': product_list})
