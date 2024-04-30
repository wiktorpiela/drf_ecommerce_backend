from rest_framework import generics, status
from  django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImages
from .serializers import ProductSerializer, ReviewSerializer
from .filters import ProductsFilter
from .paginators import ProductPaginator
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Product deleted successfully"})
    
class ReviewCreateUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pass