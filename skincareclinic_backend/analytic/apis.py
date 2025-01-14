from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from rest_framework import status
from django.db.models import Sum, F


@api_view(['GET'])
def get_analytics(request):
    filter = request.GET.get('filter', 'all_time')

    now = datetime.now()
    start_date = None

    if filter not in ['all_time', '7_days', '30_days', '6_months', '1_year']:
        return Response({'error': 'Invalid filter value'}, status=status.HTTP_400_BAD_REQUEST)

    if filter == '7_days':
        start_date = now - timedelta(days=7)
    elif filter == '30_days':
        start_date = now - timedelta(days=30)
    elif filter == '6_months':
        start_date = now - timedelta(days=6 * 30)
    elif filter == '1_year':
        start_date = now - timedelta(days=365)

    if start_date:
        sales_data = get_sales_data(start_date)
        sales_serializer = OrderSerializer(sales_data, many=True)
        products = get_most_sold(start_date)
        category = get_most_category(start_date)

        return Response({'sales': sales_serializer.data, 'products': products, 'category': category})

    return Response({'error': 'Unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_sales_data(start_date):
    sales_data = Order.objects.filter(created_at__gte=start_date, paid=True)
    return sales_data


def get_most_sold(start_date):
    most_sold_items = OrderItem.objects.filter(
        order__created_at__gte=start_date, order__paid=True
    ).values(
        'product__thumbnail',
        'product__name',
        'product_id',
        'product__price'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    ).order_by('-total_quantity')[:5]

    # Return an empty list if no data is found
    result = []
    for item in most_sold_items:
        product = {
            'name': item['product__name'],
            'sales': item['total_quantity'],
            'revenue': float(item['total_revenue']),  # Use the calculated total revenue
            'image': f"http://127.0.0.1:8000/media/{item['product__thumbnail']}" if item['product__thumbnail'] else 'https://placehold.co/300'
        }
        result.append(product)

    return result


def get_most_category(start_date):
    most_category = OrderItem.objects.filter(
        order__created_at__gte=start_date, order__paid=True
    ).values(
        'product__category__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:4]

    # Return an empty list if no data is found
    result = []
    for item in most_category:
        category = {
            'name': item['product__category__name'],
            'value': item['total_quantity']
        }
        result.append(category)

    return result
