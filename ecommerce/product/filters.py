from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from .models import Product

class ProductsFilter(FilterSet):

    keyword = CharFilter(field_name='name', lookup_expr='icontains')
    min_price = NumberFilter(field_name='price' or 0, lookup_expr='gte')
    max_price = NumberFilter(field_name='price' or 10000000, lookup_expr='lte')

    class Meta:
        model = Product
        fileds = ('keyword', 'category', 'brand', 'min_price', 'max_price',)
        exclude = ('created_at',)