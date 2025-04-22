from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime , timedelta
from order.models import OrderItem , Order
from order.serializers import OrderSerializer
from rest_framework import status
from django.db.models import Sum, F, FloatField, Value
from django.utils.dateparse import parse_date
from django.db.models.functions import Cast , Replace




@api_view(['GET'])
def get_unprocessed_orders(request):
    
    orders = Order.objects.filter(paid=True, status=Order.RECEIVED)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_analytics(request):


    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')


    try:
        start_date = parse_date(start_date_str) if start_date_str else None

        end_date = parse_date(end_date_str) if end_date_str else None

        if not start_date and not end_date:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)

        elif not start_date:
            start_date = end_date - timedelta(days=30)
        elif not end_date:
            end_date = datetime.now().date()


        if start_date > end_date:
            return Response(
                {'error':'Start data cannot be after end date'},
                status=status.HTTP_400_BAD_REQUEST
                
            )
        
    except (ValueError,TypeError) as e:
        return Response(
            {'error':'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

    #Get data for the data range

    try:

        # Get sales data
        sales_data = get_sales_data(start_date)
        

        #Get most sold products with proper thumbnail handling

        products = get_most_sold(start_date,end_date)


        # Get Category distribution
        category = get_most_category(start_date, end_date)

        return Response({
            'products':products,
            'category':category,
            'sales_data': sales_data,
            'date_range':{
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')

            }
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    



def get_sales_data(start_date):
    sales_data = Order.objects.filter(created_at__gte=start_date, paid=True)
    total_order = sales_data.count()
    total_revenue = sales_data.aggregate(
        total_revenue=Sum(Cast(Replace(F('order_amount'), Value(','), Value('')), output_field=FloatField()))
    ).get('total_revenue', 0)


    return {
        'total_order': total_order,
        'total_revenue': float(total_revenue or 0),
    }



def get_most_category(start_date, end_date):
    most_category = OrderItem.objects.filter(
        order__created_at__date__gte = start_date,
        order__created_at__date__lte=end_date,
        order__paid=True

    ).values(
        'category_name',
    ).annotate(
        total_quantity = Sum('quantity'),
        total_revenue=Sum(Cast(Replace(F('price'),Value(','),Value('')), output_field=FloatField()) )
    ).order_by('-total_quantity')[:5]


    return [{
        'name': item['category_name'] or 'Uncategorizes',
        'value': float(item['total_revenue'] or 0)
    } for item in most_category]





def get_most_sold(start_date, end_date):
    most_sold = OrderItem.objects.filter(
        order__created_at__date__gte=start_date,
        order__created_at__date__lte=end_date,
        order__paid=True
    ).values(
        'product_name',
        'brand_name',
        'category_name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(Cast(Replace(F('price'), Value(','), Value('')), output_field=FloatField()))
    ).order_by('-total_quantity')[:5]

    return [{
        'product_name': item['product_name'],
        'brand_name': item['brand_name'],
        'category_name': item['category_name'] or 'Uncategorized',
        'total_quantity': item['total_quantity'],
        'total_revenue': float(item['total_revenue'] or 0)
    } for item in most_sold]

  






