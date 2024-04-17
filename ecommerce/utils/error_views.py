from rest_framework import status
from django.http import JsonResponse

def handler404(request, exception):
    response = JsonResponse(data={'error': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)
    return response

def handler500(request):
    response = JsonResponse(data={'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response