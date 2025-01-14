from django.urls import path
from . import apis

urlpatterns = [
    path('annoucements/', apis.get_annoucement, name='get_annoucement')
]