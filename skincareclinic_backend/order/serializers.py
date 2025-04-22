from rest_framework import serializers
from .models import Order, OrderItem
from shop.serializers import ProductSerializer




class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only =True)

    class Meta:
        model = Order
        fields = ('id','full_name','created_at','order_amount','paid','status', 'has_refund')


    
   

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price_value = serializers.SerializerMethodField()
    order = OrderSerializer()
    
    class Meta:
        model = OrderItem
        fields = ('__all__')

    
    def get_price_value(self,obj):
        return float(obj.price.replace(',',''))






        
    
    
    

