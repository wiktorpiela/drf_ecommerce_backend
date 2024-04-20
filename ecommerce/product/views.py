from rest_framework import generics
from  django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImages
from .serializers import ProductSerializer, ProductImagesSerializer
from .filters import ProductsFilter
from .paginators import ProductPaginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsProductOwnerOrReadOnly


class Products(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #pagination_class = ProductPaginator

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()

