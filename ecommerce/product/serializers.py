from rest_framework import serializers
from .models import *

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    images = ProductImagesSerializer(many=True, read_only=True, required=False)

    class Meta:
        model=Product
        fields = ('name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'created_at', 'images',)

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images') 
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImages.objects.create(product=product, image=image_data)

        return product
