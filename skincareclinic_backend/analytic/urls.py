from django.urls import path

from .apis import get_analytics , get_unprocessed_orders


urlpatterns = [
    path('get_analytics', get_analytics, name='get_analytics'),
    path('unprocessed_orders', get_unprocessed_orders, name='unprocessed_orders'),
]