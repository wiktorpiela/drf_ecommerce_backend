from rest_framework import generics, status
from  django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImages, Review
from .serializers import ProductSerializer, ReviewSerializer
from rest_framework.decorators import permission_classes
from .filters import ProductsFilter
from .paginators import ProductPaginator
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

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
    permission_classes = [IsOwnerOrReadOnly]

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
            product = Product.objects.get(id=request.data['product'])
            review = product.review.filter(user=self.request.user)

            if review.exists():
                new_review = {'rating': request.data['rating'], 'comment': request.data['comment']}
                review.update(**new_review)
                rating = product.review.aggregate(avg_ratings = Avg('rating'))
                product.ratings = rating['avg_ratings']
                product.save()
                return Response({'message': 'Review successfully updated'}, status=status.HTTP_200_OK)
            
            elif product.user == self.request.user:
                return Response({'error': 'You are not allowed to post review to your own product.'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)