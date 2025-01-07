from rest_framework import serializers
from .models import DeliveryCategory, Delivery

class DeliveryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCategory
        fields = '__all__'



class DeliverySerializer(serializers.ModelSerializer):
    category = DeliveryCategorySerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ('id','name', 'slug','category','weight_from','weight_to','price')