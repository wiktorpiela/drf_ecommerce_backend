from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('users/', UserList.as_view(), name='usersView')

]

