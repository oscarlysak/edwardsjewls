# shop/views.py
from django.shortcuts import render
from products.models import ProductCategory, Products, ProductImage, ProductStyle, ProductCondition
from django.http import JsonResponse
from django.db.models import Q
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def get_fuzzy_matches(query, choices, scorer=fuzz.partial_ratio, cutoff=60): # to adjust typo tolerance, change the cutoff value
    """
    Return the best matches for a given query using fuzzy matching.
    """
    return process.extractBests(query, choices, scorer=scorer, score_cutoff=cutoff)

def shop(request):
    search_query = request.GET.get('q', '')

    products = Products.objects.all()
    categories = ProductCategory.objects.all()
    styles = ProductStyle.objects.all()

    if search_query:
        product_names = products.values_list('name', flat=True)
        product_descriptions = products.values_list('description', flat=True)
        category_names = categories.values_list('name', flat=True)
        category_descriptions = categories.values_list('description', flat=True)
        style_names = styles.values_list('name', flat=True)
        style_descriptions = styles.values_list('description', flat=True)

        product_matches = get_fuzzy_matches(search_query, product_names) + get_fuzzy_matches(search_query, product_descriptions)
        category_matches = get_fuzzy_matches(search_query, category_names) + get_fuzzy_matches(search_query, category_descriptions)
        style_matches = get_fuzzy_matches(search_query, style_names) + get_fuzzy_matches(search_query, style_descriptions)

        matched_product_ids = [Products.objects.get(name=match[0]).id for match in product_matches if match[0] in product_names] + \
                              [Products.objects.get(description=match[0]).id for match in product_matches if match[0] in product_descriptions]
        matched_category_ids = [ProductCategory.objects.get(name=match[0]).id for match in category_matches if match[0] in category_names] + \
                               [ProductCategory.objects.get(description=match[0]).id for match in category_matches if match[0] in category_descriptions]
        matched_style_ids = [ProductStyle.objects.get(name=match[0]).id for match in style_matches if match[0] in style_names] + \
                            [ProductStyle.objects.get(description=match[0]).id for match in style_matches if match[0] in style_descriptions]

        filters = Q(id__in=matched_product_ids) | Q(product_category_id__in=matched_category_ids) | Q(product_style_id__in=matched_style_ids)
        products = products.filter(filters)

    images = ProductImage.objects.all()
    return render(request, 'shop/shop.html', {'products': products, 'categories': categories, 'styles': styles, 'images': images})

def filter_products(request):
    category_id = request.GET.get('category_id')
    style_id = request.GET.get('style_id')
    search_query = request.GET.get('q', '')

    products = Products.objects.all()

    if search_query:
        product_names = products.values_list('name', flat=True)
        product_descriptions = products.values_list('description', flat=True)
        category_names = ProductCategory.objects.values_list('name', flat=True)
        category_descriptions = ProductCategory.objects.values_list('description', flat=True)
        style_names = ProductStyle.objects.values_list('name', flat=True)
        style_descriptions = ProductStyle.objects.values_list('description', flat=True)

        product_matches = get_fuzzy_matches(search_query, product_names) + get_fuzzy_matches(search_query, product_descriptions)
        category_matches = get_fuzzy_matches(search_query, category_names) + get_fuzzy_matches(search_query, category_descriptions)
        style_matches = get_fuzzy_matches(search_query, style_names) + get_fuzzy_matches(search_query, style_descriptions)

        matched_product_ids = [Products.objects.get(name=match[0]).id for match in product_matches if match[0] in product_names] + \
                              [Products.objects.get(description=match[0]).id for match in product_matches if match[0] in product_descriptions]
        matched_category_ids = [ProductCategory.objects.get(name=match[0]).id for match in category_matches if match[0] in category_names] + \
                               [ProductCategory.objects.get(description=match[0]).id for match in category_matches if match[0] in category_descriptions]
        matched_style_ids = [ProductStyle.objects.get(name=match[0]).id for match in style_matches if match[0] in style_names] + \
                            [ProductStyle.objects.get(description=match[0]).id for match in style_matches if match[0] in style_descriptions]

        filters = Q(id__in=matched_product_ids) | Q(product_category_id__in=matched_category_ids) | Q(product_style_id__in=matched_style_ids)
        products = products.filter(filters)
    
    if category_id:
        products = products.filter(product_category_id=category_id)
    if style_id:
        products = products.filter(product_style_id=style_id)
    
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
