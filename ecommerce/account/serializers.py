from rest_framework import serializers
from django.contrib.auth.models import User
from product.serializers import ProductSerializer

class UserSerializer(serializers.ModelSerializer):
    user_products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_products',)
