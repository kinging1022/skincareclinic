from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import status
from shop.models import Product
from .models import Order
from .utils import process_checkout
from django.conf import settings




@api_view(['POST'])
def track_order(request):
    tracking = request.data.get('tracking')

    try:
        order = Order.objects.get(transaction_ref=tracking)
    
    except Order.DoesNotExist:
        return Response({'error':'order does not exist'},status=status.HTTP_404_NOT_FOUND)
 

    status = order.status

    return Response({'status':status})





def format_price(price):
    price = float(price)
    return f'{price:,.2f}'


@api_view(['POST'])
def checkout(request):
    items = request.data.get('items')

    insufficient_products = []
    total = 0
    total_weight = 0

    # Check if the quantity of the items is available
    for item in items:
        product_id = item['product']
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']

        if product.stock < quantity:
            insufficient_products.append({'name': product.name,
                                         'stock': product.stock
                                         })
            
        total += product.price * quantity
        total_weight += product.weight * quantity

    if insufficient_products:
        return Response({'error': 'some products are not available in stock', 'insufficient_products': insufficient_products}, status=status.HTTP_400_BAD_REQUEST)
    
    shipping = request.data.get('shipping_fee')
    total_with_shipping = total + shipping

    order_id = process_checkout(
                          full_name=request.data.get('full_name'),
                          email=request.data.get('email'), 
                          address=request.data.get('address'), 
                          phone=request.data.get('phone_number'), 
                          weight= total_weight,
                          order_amount=total, 
                          shipping_fee= format_price(shipping), 
                          order_amount_with_shipping=format_price(total_with_shipping), 
                          delivery_method=request.data.get('delivery_option'), 
                          delivery_area=request.data.get('delivery_location'), 
                          items=items,
    )

    try:
        # Paystack API endpoint
        url = "https://api.paystack.co/transaction/initialize"

        metadata = {
            "order_id": order_id,
            "cancel_action": "http://localhost:5173/payment-failed",
        }

        

        session_data = {
            'email': request.data.get('email'), 
            'amount': float(total_with_shipping) * 100,  # Amount in kobo
            'metadata': metadata,
            'callback_url': f'http://localhost:5173/payment-success/{order_id}'
        }

        # Set up headers with Paystack secret key
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}


        #make api request
        response = requests.post(url, headers=headers, json=session_data)
        response_data = response.json()

        if response.status_code == 200 and response_data['status'] == True:
            redirect_url = response_data['data']['authorization_url']
            return Response({'redirect_url': redirect_url}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': response_data['message']}, status=status.HTTP_400_BAD_REQUEST)


    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

