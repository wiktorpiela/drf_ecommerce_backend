from rest_framework import generics, permissions

from .serializers import UserSerializer
from django.contrib.auth.models import User


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        return [permissions.AllowAny() if self.request.method=='POST' else permissions.IsAdminUser()]

