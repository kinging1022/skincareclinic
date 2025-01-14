from rest_framework import serializers
from .models import Annoucement

class AnnoucementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annoucement
        fields = ['id', 'title']  