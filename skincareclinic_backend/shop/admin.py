from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product, Collections

class ProductAdmin(admin.ModelAdmin):
    filter_vertical = ('collection',) 



admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Collections)