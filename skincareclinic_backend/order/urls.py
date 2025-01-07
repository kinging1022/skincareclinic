from django.urls import path
from . import apis
from . import webhooks



urlpatterns = [
    path('checkout/', apis.checkout, name='checkout'),
    path('hooks/',webhooks.paystack_webhook, name='paystack_webhook'),
]