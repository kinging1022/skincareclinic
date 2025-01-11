from django.urls import path

from .apis import get_analytics  


urlpatterns = [
    path('get_sale_data', get_analytics, name='get_analytics'),
]