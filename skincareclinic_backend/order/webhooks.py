import json
import hashlib
import hmac
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from shop.models import Product

def verify_signature(request_data, signature):
    secret_key = settings.PAYSTACK_SECRET_KEY
    hash = hmac.new(secret_key.encode('utf-8'), request_data, hashlib.sha512).hexdigest()
    return hash == signature

@csrf_exempt
def paystack_webhook(request):
    # Only process POST requests
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

        try:
            order = Order.objects.get(pk=order_id)
            if event['event'] == 'charge.success':
                
                
                order.paid = True

                order.transaction_ref = event['data']['reference']
                order.status = Order.RECIEVED
                order.save()

                order.send_confirmation_email()
                order.send_order_created()

                # Update product stock
                for item in order.items.all():
                    product = Product.objects.get(pk=item.product.id)
                    product.stock -= item.quantity
                    if product.stock == 0:
                        product.available = False
                    product.save()

            else:
                order.paid = False
                order.save()

                order.send_order_created()

                

            # Return a success response after processing the event
            return JsonResponse({'status': 'success', 'message': 'Order updated successfully'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Order not found'}, status=404)
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'status': 'failed', 'message': 'Invalid event data'}, status=400)
