#shop/views.py
from django.shortcuts import render
from products.models import ProductCategory, Products, ProductImage, ProductStyle
from django.http import JsonResponse

def shop(request):
    categories = ProductCategory.objects.all()
    styles = ProductStyle.objects.all()
    products = Products.objects.all()
    images = ProductImage.objects.all()
    return render(request, 'shop/shop.html', {'categories': categories, 'styles': styles, 'products': products, 'images': images})

def filter_products(request):
    category_id = request.GET.get('category_id')
    style_id = request.GET.get('style_id')
    print(f"Filtering by category: {category_id}, style: {style_id}")  # Debug print
    
    filters = {}
    if category_id:
        filters['product_category_id'] = category_id
    if style_id:
        filters['product_style_id'] = style_id

    products = Products.objects.filter(**filters) if filters else Products.objects.all()
    
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

