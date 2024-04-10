from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model=Product
        fields = ('name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'created_at',)