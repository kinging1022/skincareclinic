from rest_framework import serializers
from .models import Order, OrderItem
from shop.serializers import ProductSerializer




class OrderSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id','date','value','paid','status')


    def get_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    
    def get_value(self,obj):
        return float(obj.order_amount.replace(',',''))
    


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price_value = serializers.SerializerMethodField()
    order = OrderSerializer()
    
    class Meta:
        model = OrderItem
        fields = ('__all__')

    
    def get_price_value(self,obj):
        return float(obj.price.replace(',',''))






        
    
    
    

