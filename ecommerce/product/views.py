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
            rating = int(request.data['rating'])
            product = Product.objects.get(id = request.data['product'])
            review = product.review.filter(user=self.request.user)

            if rating < 1 or rating > 5:
                return Response({'message': 'Rating must be an integer between 1 and 5 included'}, status=status.HTTP_400_BAD_REQUEST)
            
            if review.exists():
                new_review = {
                    'rating': request.data['rating'],
                    'comment': request.data['comment'],
                }
                review.update(**new_review)
                rating = product.review.aggregate(avg_rating=Avg('rating'))
                product.rating = rating['avg_rating']
                product.save()

            else:
                serializer.save(user=self.request.user)
                

            return Response(status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pass