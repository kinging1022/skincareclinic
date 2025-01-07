from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
admin.site.register(OrderItem)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'email', 'address', 'phone',
        'created_at', 'weight', 'order_amount', 'shipping_fee',
        'order_amount_with_shipping', 'delivery_method', 'delivery_area',
        'paid', 'transaction_ref', 'shipped_date', 'status'
    )
