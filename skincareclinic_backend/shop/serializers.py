from rest_framework import serializers
from .models import Product, Category, Brand, Collections


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug','get_image', 'get_thumbnail',)



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('id', 'name', 'slug','get_image', 'get_thumbnail',)






class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug')



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'brand', 'description', 'price', 'get_image', 'get_thumbnail', 'available', 'stock', 'weight', 'created', 'updated','featured')
        