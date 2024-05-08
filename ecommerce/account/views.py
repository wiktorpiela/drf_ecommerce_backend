from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .utils.account_utils import get_current_host
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        return [permissions.AllowAny() if self.request.method=='POST' else permissions.IsAdminUser()]
    
class ForgotPassword(APIView):

    def post(self, request, format=None):
        data = request.data
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({'message': 'User doesnt exist!'})
        
        token = get_random_string(40)
        expire_date = datetime.now() + timedelta(minutes=30)

        user.profile.reset_password_token = token
        user.profile.reset_password_expire = expire_date

        user.profile.save()

        host = get_current_host(request)
        link = f'{host}/account/reset-password/{token}/'
        body = f"Your password reset link is: {link}"

        email = EmailMessage(
            subject=f'Password reset for eShop',
            body = body,
            from_email= settings.DEFAULT_FROM_EMAIL,
            to=[data['email']])
        email.content_subtype = "html"
        email.send(fail_silently=False)

        return Response({'message': f"Password reset email sent to {data['email']}"})
    
class ResetPassword(APIView):
    
    def post(self, request, token, format=None):
        data = request.data
        try:
            user = User.objects.get(profile__reset_password_token=token)
        except User.DoesNotExist:
            return Response({'message': 'User doesnt exist!'}, status=status.HTTP_400_BAD_REQUEST)

        if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
            return Response({'message': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        if data['password'] != data['confirm_password']:
            return Response({'message': 'Passwords missmatch'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(data['password'])
        user.profile.reset_password_token = ''
        user.profile.reset_password_expire = None

        user.profile.save()
        user.save()

        return Response({'message': 'Password has been successfully changed'}, status=status.HTTP_200_OK)

