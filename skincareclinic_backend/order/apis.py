from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from shop.models import Product
from .models import Order
from .serializers import OrderSerializer
from delivery.models import Delivery
from .utils import process_checkout
from .utils import initialize_paystack_session
import logging
from django.utils import timezone
import re

logger = logging.getLogger(__name__)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def format_price(price):
    try:
        return f'{float(price):,.2f}'
    except (ValueError, TypeError):
        return "0.00"


@api_view(['POST'])
def track_order(request):
    tracking = request.data.get('tracking')

    if not tracking:
        return Response({'error': 'Tracking reference required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(transaction_ref=tracking)
    except Order.DoesNotExist:
        return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order)

    return Response(serializer.data,status=status.HTTP_200_OK)

def validate_email(email):
    return re.match(EMAIL_REGEX, email) is not None


def validate_delivery(data):
    if not all(data.get(field)  for field in ['address','delivery_location']):
        return Response( {'error': 'Address and delivery location are required for delivery'},
            status=status.HTTP_400_BAD_REQUEST)
    
    try:
        shipping_fee = int(data.get('shipping_fee', 0))
        if shipping_fee <= 0:
            return Response(
                {'error': 'Shipping fee must be a positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        delivery = Delivery.objects.get(name=data['delivery_location'], price=shipping_fee)
        if delivery.price != shipping_fee:
            return Response(
                {'error': 'Shipping fee does not match selected location'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return shipping_fee
    except Delivery.DoesNotExist:
        return Response(
            {'error': 'Invalid delivery location'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except (ValueError, TypeError):
        return Response(
            {'error': 'Invalid shipping fee format'},
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(['POST'])
def checkout(request):
    data = request.data

    # Validate required fields

    required_fields = ['full_name', 'email', 'phone_number', 'delivery_option']

    if not all(data.get(field) for field in required_fields):
        return Response(
            {'error': 'All required fields must be provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

    # Email validation
    if not validate_email(data['email']):
        return Response(
            {'error': 'Please enter a valid email address'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

    #validate item
    items = data.get('items',[])

    if not isinstance(items,list):
        return Response(
            {'error': 'Items must be provided as a list'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

    # Process delivery option
    if data['delivery_option'] == 'delivery':
        validation_result = validate_delivery(data)

        if isinstance(validation_result, Response):
            return validation_result
        
        shipping_fee = validation_result

    else:
        shipping_fee = 0
        data.update({
            'address': "",
            'delivery_location': "",
            'shipping_fee': 0
        })





     # Process items and calculate totals
    insufficient_products = []
    total = 0
    total_weight = 0

    for item in items:
        try:
            product = Product.objects.get(id=item['product'])
            quantity = int(item['quantity'])
            
            if product.stock < quantity:
                insufficient_products.append({
                    'name': product.name,
                    'stock': product.stock
                })
            
            total += product.price * quantity
            total_weight += product.weight * quantity
            
        except (KeyError, ValueError, TypeError, Product.DoesNotExist):
            return Response(
                {'error': f'Invalid product data for item: {item}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    if insufficient_products:
        return Response({
            'error': 'Some products are not available in stock',
            'insufficient_products': insufficient_products
        }, status=status.HTTP_400_BAD_REQUEST)
    

    # Create order and initialize payment
    try:
        order_id = process_checkout(
            full_name=data['full_name'],
            email=data['email'],
            address=data['address'],
            phone=data['phone_number'],
            weight=total_weight,
            order_amount=format_price(total),
            shipping_fee=format_price(shipping_fee),
            order_amount_with_shipping=format_price(total + shipping_fee),
            delivery_method=data['delivery_option'],
            delivery_area=data.get('delivery_location', ''),
            items=items
        )

        response = initialize_paystack_session(
            data['email'],
            total + shipping_fee,
            order_id
        )
        response_data = response.json()

        if response.status_code == 200 and response_data['status']:
            return Response(
                {'redirect_url': response_data['data']['authorization_url']},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': response_data.get('message', 'Payment initialization failed')},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        logger.exception(f"Checkout failed: {str(e)}")
        return Response(
            {'error': 'An error occurred during checkout'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status(request):
    order_id = request.data.get('id')
    action = request.data.get('action')

    if not order_id or not action:
        return Response(
            {'error': 'Both order ID and action are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Define status transitions
    status_transitions = {
        'set_processed': {
            'new_status': Order.PROCESSED,
            'valid_current_statuses': [Order.RECEIVED],
            'actions': lambda o: None  # No additional actions needed
        },
        'set_shipped': {
            'new_status': Order.SENT,
            'valid_current_statuses': [Order.PROCESSED],
            'actions': lambda o: [
                setattr(o, 'shipped_date', timezone.now()),  # Correct way to set attribute
                o.send_order_sent()
            ]
        }
    }

    if action not in status_transitions:
        return Response(
            {'error': 'Invalid action'},
            status=status.HTTP_400_BAD_REQUEST
        )

    transition = status_transitions[action]
    if (transition.get('valid_current_statuses') and 
        (order.status not in transition['valid_current_statuses'])):
        return Response(
            {'error': f'Order must be in {transition["valid_current_statuses"]} to perform this action'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order.status = transition['new_status']
        if transition['actions'](order):  # Execute additional actions
            pass
        order.save()
        
        return Response(
            {
                'message': f'Order status updated to {order.get_status_display()}',
                'new_status': order.status
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )