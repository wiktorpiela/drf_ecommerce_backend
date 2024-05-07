from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .utils.account_utils import get_current_host
from django.core.mail import send_mail


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
        link = f'{host}/api/reset_password/token'
        body = f"Your password reset link is: {link}"

        send_mail(
            'Password reset for eShop',
            body,
            'noreply@eshop.com',
            [data['email']],
        )

        return Response({'message': f"Password reset email sent to {data['email']}"})

