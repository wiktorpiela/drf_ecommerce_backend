from django.urls import path
from .views import *

app_name='order'
urlpatterns = [
    path('order/new/', NewOrder.as_view(), name='new_order')
]