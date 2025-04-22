import json
import hashlib
import hmac
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Order, Refund
from shop.models import Product
import logging

logger = logging.getLogger(__name__)


def verify_signature(request_data, signature):
    secret_key = settings.PAYSTACK_SECRET_KEY
    hash = hmac.new(secret_key.encode('utf-8'), request_data, hashlib.sha512).hexdigest()
    return hash == signature



def adjust_stock_and_create_refund(order, product, quantity):
    """
    Returns tuple: (success: bool, refund_quantity: int)
    Note: This function assumes it's called within an existing transaction
    """

    refund_quantity = 0
    product = Product.objects.select_for_update().get(pk=product.id)

    if product.stock >= quantity:
        product.stock -= quantity
        if product.stock == 0:
            product.available = False
        product.save()
        return True,0
    
    sold_quantity = product.stock
    refund_quantity = quantity - sold_quantity
    product.stock = 0
    product.available = False
    product.save()

    Refund.objects.create(
        order=order,
        customer_name=order.full_name,
        customer_email=order.email,     
        customer_phone=order.phone,
        product=product.name,
        quantity=refund_quantity,
        price=product.price * refund_quantity,
        refunded=False
    )
    return False, refund_quantity



@csrf_exempt
def paystack_webhook(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

    request_data = request.body
    signature = request.headers.get('X-Paystack-Signature')

    if not verify_signature(request_data, signature):
        return JsonResponse({'status': 'failed', 'message': 'Invalid signature'}, status=400)

    try:
        event = json.loads(request_data)
        metadata = event['data']['metadata']
        order_id = metadata.get('order_id', '')

        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=order_id)
                
                if event['event'] == 'charge.success':
                    # Check if already processed to make idempotent
                    if order.paid and order.transaction_ref:
                        return JsonResponse({'status': 'success', 'message': 'Order already processed'})
                    
                    order.paid = True
                    order.transaction_ref = event['data']['reference']
                    order.status = Order.RECEIVED  
                    has_refund = False

                    for item in order.items.select_related('product').all():
                        try:
                            success, refund_quantity = adjust_stock_and_create_refund(
                                order, 
                                item.product,
                                item.quantity
                            )
                            if not success:
                                has_refund = True
                        except Product.DoesNotExist:
                            logger.error(f"Product not found for order {order_id}")
                            continue

                    order.has_refund = has_refund
                    order.save()

                    # Defer emails until after successful commit
                    transaction.on_commit(
                        lambda: order.send_all_emails()
                    )

                    return JsonResponse({'status': 'success'}, status=200)
                
                else:  # Handle other events
                    order.paid = False
                    order.save()
                    order.send_order_created()
                    return JsonResponse({'status': 'success'}, status=200)

            except Order.DoesNotExist:
                logger.error(f"Order not found: {order_id}")
                return JsonResponse({'status': 'failed', 'message': 'Order not found'}, status=404)
                
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        return JsonResponse({'status': 'failed', 'message': 'Invalid event data'}, status=400)