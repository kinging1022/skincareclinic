from django.contrib import admin
from .models import Delivery, DeliveryCategory

# Register your models here.
admin.site.register(DeliveryCategory)
admin.site.register(Delivery)
