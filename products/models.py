from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.URLField(max_length=500, blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sizes = models.CharField(max_length=100, default='XS,S,M,L,XL')
    colors = models.CharField(max_length=200, default='Black,White,Blue')
    is_new = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name