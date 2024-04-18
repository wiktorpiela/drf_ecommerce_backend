from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('product.urls')),
    path('api-token-auth/', views.obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)

handler404 = 'utils.error_views.handler404'
handler500 = 'utils.error_views.handler500'