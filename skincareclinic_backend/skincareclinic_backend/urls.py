"""
URL configuration for skincareclinic_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from shop.views import fake_admin
from django.conf.urls.static import static
 
urlpatterns = [
    path('secure/admin/2015/', admin.site.urls),
    path('admin/',fake_admin,name='fake_admin'),
    path('api/', include('shop.urls')),
    path('api/', include('delivery.urls')),
    path('api/', include('order.urls')),
    path('api/', include('analytic.urls')),
    path('api/', include('annoucement.urls')),
    path('api/', include('user.urls')),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

