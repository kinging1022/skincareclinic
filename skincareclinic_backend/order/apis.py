from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from shop.models import Product
from .models import Order
from .utils import process_checkout
from .utils import initialize_paystack_session
import logging

logger = logging.getLogger(__name__)


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

    return Response({'status': order.status})


@api_view(['POST'])
def checkout(request):
    data = request.data
    items = data.get('items')

    if not items or not isinstance(items, list):
        return Response({'error': 'Items must be provided as a list'}, status=status.HTTP_400_BAD_REQUEST)

    required_fields = ['full_name', 'email', 'address', 'phone_number', 'shipping_fee', 'delivery_option', 'delivery_location']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'{field.replace("_", " ").capitalize()} is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        shipping_fee = float(data['shipping_fee'])
    except (ValueError, TypeError):
        return Response({'error': 'Invalid shipping fee'}, status=status.HTTP_400_BAD_REQUEST)

    insufficient_products = []
    total = 0
    total_weight = 0

    for item in items:
        product_id = item.get('product')
        quantity = item.get('quantity')

        try:
            quantity = int(quantity)
            product = Product.objects.get(id=product_id)
        except (ValueError, TypeError, Product.DoesNotExist):
            return Response({'error': f'Invalid product or quantity for product ID {product_id}'}, status=status.HTTP_400_BAD_REQUEST)

        if product.stock < quantity:
            insufficient_products.append({
                'name': product.name,
                'stock': product.stock
            })

        total += product.price * quantity
        total_weight += product.weight * quantity

    if insufficient_products:
        return Response({
            'error': 'Some products are not available in stock',
            'insufficient_products': insufficient_products
        }, status=status.HTTP_400_BAD_REQUEST)

    total_with_shipping = total + shipping_fee

    # Create the order
    order_id = process_checkout(
        full_name=data['full_name'],
        email=data['email'],
        address=data['address'],
        phone=data['phone_number'],
        weight=total_weight,
        order_amount=total,
        shipping_fee=format_price(shipping_fee),
        order_amount_with_shipping=format_price(total_with_shipping),
        delivery_method=data['delivery_option'],
        delivery_area=data['delivery_location'],
        items=items
    )

    try:
        response = initialize_paystack_session(data['email'], total_with_shipping, order_id)
        response_data = response.json()

        if response.status_code == 200 and response_data['status']:
            redirect_url = response_data['data']['authorization_url']
            return Response({'redirect_url': redirect_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': response_data.get('message', 'Failed to initialize payment')}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.exception(f"Payment initialization failed: {str(e)}")
        return Response({'error': f'Payment initialization failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
