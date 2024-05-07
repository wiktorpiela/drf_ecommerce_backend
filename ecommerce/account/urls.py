from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('users/', UserList.as_view(), name='usersView'),
    path('forgot-password/', ForgotPassword.as_view(), name='ForgotPassword')

]

