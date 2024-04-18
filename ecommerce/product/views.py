from rest_framework import generics
from  django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImages
from .serializers import ProductSerializer, ProductImagesSerializer
from .filters import ProductsFilter
from .paginators import ProductPaginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions


class Products(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #pagination_class = ProductPaginator

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class ProductDetails(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['POST'])
def upload_product_images(request):
    data = request.data
    files = request.FILES.getlist('images')

    # print('files', files)
    # print('data', data)

    images = []
    for file in files:
        image = ProductImages.objects.create(product=Product(data['product']), image=file)
        images.append(image)

    serializer = ProductImagesSerializer(images, many=True)

    return Response(serializer.data)

# class UploadProductImages(generics.CreateAPIView):
#     queryset = ProductImages.objects.all()
#     serializer_class = ProductImageSerializer

#     def perform_create(self, serializer):
#         product_id = self.request.data.get('product')
#         product = Product.objects.get(pk=product_id)
#         serializer.save(product=product)