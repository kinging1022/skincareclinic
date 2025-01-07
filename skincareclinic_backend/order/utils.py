from .models import Order, OrderItem
from shop.models import Product

def format_price(price):
    price = float(price)
    return f'{price:,.2f}'

def process_checkout(full_name, email, address, phone, weight, order_amount, shipping_fee, order_amount_with_shipping, delivery_method, delivery_area, items):
    order = Order.objects.create(
                                full_name=full_name, 
                                 email=email,
                                 address=address, 
                                 phone=phone, 
                                 weight=weight,
                                 order_amount=order_amount, 
                                 shipping_fee=shipping_fee, 
                                 order_amount_with_shipping=order_amount_with_shipping, 
                                 delivery_method=delivery_method, 
                                 delivery_area=delivery_area, 
                                 )
    
    
    
    
    
    
    
    
    
    for item in items:
        product_id = item['product']
        product = Product.objects.get(id=product_id)
        price = product.price * float(item['quantity'])
        
        OrderItem.objects.create(order=order, product=product, price=format_price(price), quantity=item['quantity'])
    
    return order.id