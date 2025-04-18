import requests
from django.conf import settings
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




def initialize_paystack_session(email, amount, order_id):
    url = "https://api.paystack.co/transaction/initialize"

    metadata = {
        "order_id": order_id,
        "cancel_action": f"{settings.FRONTEND_URL}/payment-failed",
    }

    session_data = {
        "email": email,
        "amount": int(amount * 100),  # Convert to kobo
        "metadata": metadata,
        "callback_url": f"{settings.FRONTEND_URL}/payment-success/{order_id}",
    }

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=session_data, headers=headers)
    return response