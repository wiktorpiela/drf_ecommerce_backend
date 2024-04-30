from rest_framework import serializers
from django.db.models import Avg
from .models import *

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'rating', 'comment',)

        extra_kwargs = {
            'product': {'required': True},
            'rating': {'required': True},
            'comment': {'required': True}
        }

    def validate(self, data):
        product_id = data.get('product').id
        rating = data.get('rating')
        comment = data.get('comment')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product': 'Product does not exist'})
        
        if rating < 1 or rating > 5:
            raise serializers.ValidationError({'rating':'Rating an integer only from range 1 to 5.'})
        
        if not comment.strip():
            raise serializers.ValidationError({'comment': 'Comment cannot be empty'})

        return data
    
    def create(self, validated_data):
        product_id = validated_data['product'].id
        product = Product.objects.get(id=product_id)
        avg_rating = product.review.aggregate(avg_rating=Avg('rating'))

        Review.objects.create(**validated_data)
        product.ratings = avg_rating['avg_rating']
        product.save()

        return validated_data
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.user = validated_data.get('user', instance.user)

        # update mean rating in product
        product = instance.product
        avg_rating = product.review.aggregate(avg_rating=Avg('rating'))
        product.ratings = avg_rating['avg_rating']
        product.save()
        instance.save()

        return instance

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    images = ProductImagesSerializer(many=True, read_only=True, required=False)
    review = ReviewSerializer(many=True, read_only=True, required=False)

    class Meta:
        model=Product
        fields = ('id', 'name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'created_at', 'images', 'review',)

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
    

