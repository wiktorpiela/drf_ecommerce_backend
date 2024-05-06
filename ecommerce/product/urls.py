from django.urls import path
from . import views 

app_name = 'product'

urlpatterns = [
    path('all-products/', views.Products.as_view(), name='allProducts'),
    path('product-details/<int:pk>/', views.ProductDetails.as_view(), name='productDetails'),
    path('product-review-create/', views.ReviewCreateUpdate.as_view(), name='productReviewCreate'),
    path('product-review-delete/<int:pk>/', views.ReviewCreateUpdate.as_view(), name='productReviewDelete'),
]