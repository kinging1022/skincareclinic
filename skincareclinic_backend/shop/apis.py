from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category, Brand
from .serializers import ProductSerializer , CategorySerializer ,BrandSerializer

from django.db.models import Q



@api_view(['POST'])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_staff:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })



@api_view(['GET'])
def all_products(request):
    products = Product.objects.all()[:100]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
def featured_products(request):
    featured_products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(featured_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
def new_arrivals(request):
    new_arrivals = Product.objects.order_by('-created')[:10]
    serializer = ProductSerializer(new_arrivals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_detail(request,slug):
    product = Product.objects.get(slug=slug)
    product.views += 1
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def popular_products(request):
    popular_products = Product.objects.order_by('-views')[:10]
    serializer = ProductSerializer(popular_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_brand(request):
    brand = Brand.objects.all()
    serializer = BrandSerializer(brand, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_filtered_products(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')
    print(category)
    
    products = Product.objects.all()

    if category:
        products = products.filter(category__slug=category)
    if brand:
        products = products.filter(brand__slug=brand)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request):
    query = request.GET.get('query')

    products = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query) | Q(brand__name__icontains = query) | Q(description__icontains=query))

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)