from rest_framework import serializers
from .models import *

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model=Product
        fields = ('name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'created_at', 'images',)
