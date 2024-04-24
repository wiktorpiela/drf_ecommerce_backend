from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
from product.serializers import ProductSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    user_products = ProductSerializer(many=True, read_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_products',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        try:
            validate_password(password)
        except ValidationError as e:
            raise exceptions.ValidationError(e)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)

        return user
    
    def update(self, instance, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        try:
            validate_password(password)
        except ValidationError as e:
            raise exceptions.ValidationError(e)
        else:
            instance.username = username
            instance.set_password(password)
            instance.email = email
            instance.save()
            return instance