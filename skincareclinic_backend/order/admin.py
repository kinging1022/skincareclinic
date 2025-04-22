from django.contrib import admin
from .models import Order, OrderItem , Refund
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone



# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem



def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_order_pdf', args=[obj.id])))


order_pdf.short_description = 'PDF'


def admin_order_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = timezone.now()
        order.status = Order.SENT
        order.save()
        order.send_order_sent()

admin_order_shipped.short_description = 'Set shipped'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'created_at', 'paid', 'transaction_ref',  'status','delivery_method' ,order_pdf ]
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInline]
    actions=[admin_order_shipped]
       
    



admin.site.register(Order,OrderAdmin)

admin.site.register(OrderItem)

admin.site.register(Refund)
