from django.urls import path 

from rest_framework_simplejwt.views import TokenRefreshView
from .api import CustomTokenObtainPairView , PasswordResetRequest, ResetPassword
 
urlpatterns = [
    path('token/',CustomTokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request/password/reset/', PasswordResetRequest.as_view(), name='request-password-reset'),
    path('reset/password/', ResetPassword.as_view(), name='reset-password'),
   
]
