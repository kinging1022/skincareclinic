from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Annoucement
from .serializers import AnnoucementSerializer
from django.http import JsonResponse

@api_view(['GET'])
def get_annoucement(request):
    announcements = Annoucement.objects.all()

    if not announcements:
        return JsonResponse({'error': 'No announcements found'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AnnoucementSerializer(announcements, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
