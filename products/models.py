from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    SKU = models.CharField(max_length=100)
    quantity = models.IntegerField()
    
    product_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    product_condition = models.ForeignKey('ProductCondition', on_delete=models.CASCADE)
    product_style = models.ForeignKey('ProductStyle', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductCondition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductStyle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} Image"
