from django.shortcuts import render , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Order





@login_required

def admin_order_pdf(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, pk=order_id)
        pdf = order.generate_pdf()

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            content = f"attachment; filename='{order_id}.pdf"
            response['Content-Disposition'] = content

            return response
        
    return HttpResponse("Not found")
    


