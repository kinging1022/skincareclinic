from django.urls import path
from . import apis

urlpatterns = [
    path('delivery_category/', apis.get_delivery_categories, name='delivery_category'),
    path('delivery_prices/', apis.get_delivery_price, name='delivery_price'),

]