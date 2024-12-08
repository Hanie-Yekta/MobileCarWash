from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import ServicesSerializer, DetailServiceSerializer
from .models import Services



class ServicesView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint is used to show services list ",
        responses={200: "infos"}
    )
    def get(self, request):
        services = Services.objects.all()
        ser_data = ServicesSerializer(instance=services, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ServicesDetailView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint is used to show a service details ",
        responses={200: "infos"}
    )
    def get(self, request, slug):
        service = get_object_or_404(Services, slug=slug)
        ser_data = DetailServiceSerializer(instance=service)
        return Response(ser_data.data, status=status.HTTP_200_OK)
