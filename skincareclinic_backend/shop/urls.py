from django.urls import path
from . import apis


urlpatterns = [
    path('shop/products/', apis.all_products, name='product-list'),
    path('shop/products/<str:slug>/', apis.product_detail, name='product-detail'),
    path('shop/popular_products/', apis.popular_products, name='popular-products'),
    path('shop/new_arrivals/', apis.new_arrivals, name='new-arrivals'),
    path('shop/categories/', apis.get_category, name='category-list'),
    path('shop/brands/', apis.get_brand, name='brand-list'),
    path('shop/filter_products/', apis.get_filtered_products, name='filtered-products'),
    path('shop/search/', apis.search, name='search'),
    path('shop/collections/', apis.get_collections, name='collection-list'),
    path('products/create/', apis.add_product, name='add_product')
    

]