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
        fields = ('id', 'name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'created_at', 'images',)

        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'description': {'required': True, 'allow_blank': False},
            'brand': {'required': True, 'allow_blank': False},
            'category': {'required': True, 'allow_blank': False},
        }

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images') 
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImages.objects.create(product=product, image=image_data)

        return product
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        images = instance.images.all()
        images = list(images)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.category = validated_data.get('category', instance.category)
        instance.ratings = validated_data.get('ratings', instance.ratings)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()

        for image_data in images_data:
            image = images.pop(0) if images else None
            if image:
                image.image = image_data.get('image', image.image)
                image.save()
            else:
                ProductImages.objects.create(product=instance, **image_data)

        for image in images:
            image.delete()
        return instance
    
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
