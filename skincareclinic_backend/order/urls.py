from django.urls import path
from . import apis
from . import webhooks
from .views import admin_order_pdf



urlpatterns = [
    path('checkout/', apis.checkout, name='checkout'),
    path('hooks/',webhooks.paystack_webhook, name='paystack_webhook'),
    path('track_order/', apis.track_order, name='track_order'),
    path('admin_order_pdf/<int:order_id>/',admin_order_pdf, name="admin_order_pdf"),

]