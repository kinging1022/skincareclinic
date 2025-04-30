from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category, Brand, Collections
from .serializers import ProductSerializer , CategorySerializer ,BrandSerializer,CollectionSerializer

from django.db.models import Q
from django.db import transaction



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
    collection = request.GET.get('collection')
    if collection:
        products = Product.objects.filter(collection__slug=collection)
    else:
        products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_collections(request):
    collections = Collections.objects.all()
    serializer = CollectionSerializer(collections, many=True)
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
    product.save()  
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


@api_view(['POST'])
def add_product(request):
    if not request.data:
        return Response({
            'error': 'Form data is required',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        try:
            form_data = request.data
            image_file = request.FILES.get('image')
            
            # convert string bools to python bools
            def parse_boolean(value):
                if isinstance(value, str):
                    return value.lower() == 'true'
                return bool(value)
            
            # Validate required fields
            required_field = ['name', 'category', 'brand', 'price']
            for field in required_field:
                if field not in form_data:
                    return Response(
                        {'error': f'{field} is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # create the product
            product = Product(
                name=form_data['name'],
                category_id=form_data['category'],  # Directly assign ID
                brand_id=form_data['brand'],       # Directly assign ID
                description=form_data.get('description', ''),
                price=form_data['price'],
                image=image_file,
                stock=form_data.get('stock', 0),
                weight=form_data.get('weight', 0),
                featured=parse_boolean(form_data.get('featured', False)),
                available=parse_boolean(form_data.get('available', True)),
            )
            
            product.save()
            
            # Get all collections from the request - in multipart form data, 
            # multiple values with the same key come as a list already
            collection_ids = form_data.getlist('collections')
            
            # If no collection_ids were found by getlist, try to get as single value or list
            if not collection_ids:
                collection_ids = form_data.get('collections', [])
                
                # Convert to list if it's a single value
                if collection_ids and not isinstance(collection_ids, list):
                    collection_ids = [collection_ids]
            
            # Convert all collection_ids to integers
            if collection_ids:
                collection_ids = [int(id) for id in collection_ids]
            
            # Now add all collections to the product
            if collection_ids:
                product.collection.set(collection_ids)  
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Category.DoesNotExist:
            return Response(
                {'error': 'Invalid category ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Brand.DoesNotExist:
            return Response(
                {'error': 'Invalid brand ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        


