from rest_framework import generics
from  django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class Products(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'stock']
        



class ProductDetails(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer