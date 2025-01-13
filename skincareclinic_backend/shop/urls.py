from django.urls import path
from . import apis
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('shop/products/', apis.all_products, name='product-list'),
    path('shop/products/<str:slug>/', apis.product_detail, name='product-detail'),
    path('shop/featured_products/', apis.featured_products, name='featured-products'),
    path('shop/popular_products/', apis.popular_products, name='popular-products'),
    path('shop/new_arrivals/', apis.new_arrivals, name='new-arrivals'),
    path('shop/categories/', apis.get_category, name='category-list'),
    path('shop/brands/', apis.get_brand, name='brand-list'),
    path('shop/filter_products/', apis.get_filtered_products, name='filtered-products'),
    path('shop/search/', apis.search, name='search'),
    path('auth/admin/login/', apis.admin_login, name='admin_login'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


]