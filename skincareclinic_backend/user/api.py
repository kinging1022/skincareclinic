import jwt
import datetime
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error':'username and password is required'},status=status.HTTP_400_BAD_REQUEST)


        try:
            user = User.objects.get(username=username)
            if not  user.check_password(password):
                return Response({'error':'error signing in'},status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error':'error signing in'},status=status.HTTP_400_BAD_REQUEST)
        
        response = super().post(request, *args, **kwargs)

        return response





class PasswordResetRequest(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self,request):
        
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)


        except User.DoesNotExist:
            return Response({'error':'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.now(datetime.timezone.utc)

        }

        token  = jwt.encode(payload,settings.SECRET_KEY, algorithm="HS256")

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_url}",
            "noreply@example.com",
            [email],
            fail_silently=False,
        )

        return Response({'message':'password reset link sent to your email'})

        



class ResetPassword(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not token:
            return Response({'error':'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Decode the token and get the user

            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=["HS256"])

            #Retrieve user using decoded payload

            user = User.objects.get(id=(payload['user_id']))


            #set new password

            user.set_password(new_password)
            user.save()

            return Response({'message':'Password reset succesful'},status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError:
            return Response({'error': "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)













