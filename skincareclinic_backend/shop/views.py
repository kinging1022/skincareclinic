from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.

def fake_admin(request):
    return redirect(f'{settings.FRONTEND_URL}/admin/')
