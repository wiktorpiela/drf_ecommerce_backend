from django.urls import path
from . import views 

app_name = 'product'

urlpatterns = [
    path('all-products/', views.Products.as_view(), name='allProducts'),
]