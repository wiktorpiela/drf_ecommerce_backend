from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
# from utils.error_views import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('product.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

handler404 = 'utils.error_views.handler404'
handler500 = 'utils.error_views.handler500'