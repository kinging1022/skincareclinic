from django.urls import path
from . import apis

urlpatterns = [
    path('products/', apis.all_products, name='product-list'),
    path('products/<str:slug>/', apis.product_detail, name='product-detail'),
    path('featured_products/', apis.featured_products, name='featured-products'),
    path('popular_products/', apis.popular_products, name='popular-products'),
    path('new_arrivals/', apis.new_arrivals, name='new-arrivals'),
    path('categories/', apis.get_category, name='category-list'),
    path('brands/', apis.get_brand, name='brand-list'),
    path('filter_products/', apis.get_filtered_products, name='filtered-products'),

]