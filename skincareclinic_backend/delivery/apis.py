from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryCategory, Delivery
from .serializers import DeliveryCategorySerializer, DeliverySerializer
from django.db.models import Q




@api_view(['GET'])
def get_delivery_categories(request):
    delivery_categories  = DeliveryCategory.objects.all()

    serializer = DeliveryCategorySerializer(delivery_categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_delivery_price(request):
    category = request.GET.get('category')
    weight = request.GET.get('weight')
    delivery = Delivery.objects.filter(category__slug=category).filter(
        (Q(weight_from__lte=weight) & Q(weight_to__gte=weight)) | Q(weight_from__isnull=True) | Q(weight_to__isnull=True)
    )
    serializer = DeliverySerializer(delivery, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


