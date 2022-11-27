from django.shortcuts import render
#REST Framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

# Health check API view
@api_view(['GET'])
def HealthCheck(APIView):
    return Response({'status': 'OK'}, status=status.HTTP_200_OK)

