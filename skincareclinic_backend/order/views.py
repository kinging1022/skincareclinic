from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Order

def success(request):
    transaction_id = request.GET.get('order_id', None)

    if not transaction_id:
        return HttpResponse("Transaction ID not provided", status=400)
    

    try:
        transaction = Order.objects.get(id=transaction_id)

        if not transaction.paid:
            return redirect('payment-cancel')

        context = {
            'transaction_id': transaction_id,
            'amount': transaction.order_amount_with_shipping,
            'timestamp': transaction.created_at  
        }

        return render(request, 'payments/success.html', context)

    except Order.DoesNotExist:
        return HttpResponse("Transaction not found", status=404)
    


def cancel(request):


    return render(request, 'payments/failed.html')

    