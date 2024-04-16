from django_filters.rest_framework import FilterSet, CharFilter
from .models import Product

class ProductsFilter(FilterSet):

    keyword = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fileds = ('keyword', 'category', 'brand',)
        exclude = ('created_at',)