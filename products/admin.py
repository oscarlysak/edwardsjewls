from django.contrib import admin
from .models import Products, ProductCondition, ProductCategory, ProductStyle, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductCondition)
admin.site.register(ProductCategory)
admin.site.register(ProductStyle)
admin.site.register(ProductImage)