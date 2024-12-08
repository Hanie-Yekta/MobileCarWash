from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .serializer import CustomerUserSerializer, WorkerUserSerializer, AdminUserSerializer, UserForgetPassSerializer, \
    UserRandomCodeSerializer, UserChangePasswordSerializer
from orders.serializer import OrdersSerializer
from services.serializer import CommentServiceSerializer

from .models import WorkerUser, CustomerUser, User
from orders.models import Orders
from services.models import Comment

import http.client
import json
import random
from django.db.models import Count, Q



class UserRegisterView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint allows users to sign up to the system",
        request_body=CustomerUserSerializer,
        responses={201: "user created", 400: "error message"}
    )
    def post(self, request):
        ser_data = CustomerUserSerializer(data=request.data)
        if ser_data.is_valid():
            CustomerUser.objects.create_customeruser(email=ser_data.validated_data['email'],
                                                     phone_number=ser_data.validated_data['phone_number'],
                                                     first_name=ser_data.validated_data['first_name'],
                                                     last_name=ser_data.validated_data['last_name'],
                                                     gender=ser_data.validated_data['gender'],
                                                     password=ser_data.validated_data['password'])
            return Response({'detail': 'user created'}, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerUserRegisterView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint allows workers to sign up to the system",
        request_body=WorkerUserSerializer,
        responses={201: "user created", 400: "error message"}
    )
    def post(self, request):
        ser_data = WorkerUserSerializer(data=request.data)
        if ser_data.is_valid():
            WorkerUser.objects.create_workeruser(email=ser_data.validated_data['email'],
                                                 phone_number=ser_data.validated_data['phone_number'],
                                                 first_name=ser_data.validated_data['first_name'],
                                                 last_name=ser_data.validated_data['last_name'],
                                                 gender=ser_data.validated_data['gender'],
                                                 workerID=ser_data.validated_data['workerID'],
                                                 password=ser_data.validated_data['password'])
            return Response({'detail': 'user created'}, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="This endpoint allows users to log out of the system "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={201: "logged out", 401: "Unauthorized"}
    )
    def get(self, request):
        logout(request)
        return Response({'detail': 'logged out'}, status=status.HTTP_200_OK)


class WorkerUserProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="This endpoint allows workers to see their profile (personal info, worker's 'in_progress'"
                              " services, comments about them) "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "infos", 401: "Unauthorized"}
    )
    def get(sef, request):
        if request.user.is_worker:
            user = get_object_or_404(WorkerUser, email=request.user)
            services = Orders.objects.filter(status='in_progress', worker=user)
            worker_ser_data = WorkerUserSerializer(instance=user)
            orders_ser_data = OrdersSerializer(instance=services, many=True)
            comments = Comment.objects.filter(worker=user)
            comment_ser_data = CommentServiceSerializer(instance=comments, many=True)

            return Response(data={'worker_information': worker_ser_data.data,
                                  'orders': orders_ser_data.data,
                                  'comments': comment_ser_data.data}, status=status.HTTP_200_OK)


class AdminUserProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="This endpoint allows admins to see their profile (personal info, new orders, available"
                              " workers,a list of active workers, a list of active customers) "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "infos", 401: "Unauthorized"}
    )
    def get(sef, request):
        if request.user.is_admin:
            user = get_object_or_404(User, email=request.user)
            orders = Orders.objects.exclude(status=None)
            available_workers = WorkerUser.objects.filter(is_available=True)

            active_customers = CustomerUser.objects.annotate(order_count=Count('cu_order')).order_by('-order_count')[:3]
            active_workers = WorkerUser.objects.annotate(
                completed_orders=Count('wo_order', filter=Q(wo_order__status=Orders.F))).order_by('-completed_orders')[
                             :3]
            inactive_workers = WorkerUser.objects.annotate(order_count=Count('wo_order')).filter(order_count__lt=3)

            admin_ser_data = AdminUserSerializer(instance=user)
            orders_ser_data = OrdersSerializer(instance=orders, many=True)
            workers_ser_data = WorkerUserSerializer(instance=available_workers, many=True)

            active_customers_ser_data = CustomerUserSerializer(instance=active_customers, many=True)
            active_workers_ser_data = WorkerUserSerializer(instance=active_workers, many=True)
            inactive_workers_ser_data = WorkerUserSerializer(instance=inactive_workers, many=True)

            return Response(data={'admin_information': admin_ser_data.data,
                                  'orders': orders_ser_data.data,
                                  'available_workers': workers_ser_data.data,
                                  'active_customers': active_customers_ser_data.data,
                                  'active_workers': active_workers_ser_data.data,
                                  'inactive_workers': inactive_workers_ser_data.data, }, status=status.HTTP_200_OK)


class CustomerUserProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="This endpoint allows customers to see their profile (personal info, their orders) "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "infos", 401: "Unauthorized"}
    )
    def get(self, request):
        if not (request.user.is_admin or request.user.is_worker):
            user = get_object_or_404(CustomerUser, email=request.user)
            orders = user.cu_order.all()
            customer_ser_data = CustomerUserSerializer(instance=user)
            orders_ser_data = OrdersSerializer(instance=orders, many=True)

            return Response(data={'customer_information': customer_ser_data.data,
                                  'orders': orders_ser_data.data}, status=status.HTTP_200_OK)


class GetUserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="This endpoint show all user info that requested",
        responses={200: "infos", 401: "Unauthorized"}
    )
    def get(self, request):
        if request.user.is_admin:
            user = get_object_or_404(User, email=request.user)
            admin_ser_data = AdminUserSerializer(instance=user)
            return Response(data=admin_ser_data.data, status=status.HTTP_200_OK)

        elif request.user.is_worker:
            user = get_object_or_404(WorkerUser, email=request.user)
            worker_ser_data = WorkerUserSerializer(instance=user)
            return Response(data=worker_ser_data.data, status=status.HTTP_200_OK)

        else:
            user = get_object_or_404(CustomerUser, email=request.user)
            customer_ser_data = CustomerUserSerializer(instance=user)
            return Response(data=customer_ser_data.data, status=status.HTTP_200_OK)


class ForgetPasswordView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint allows users to request for change their password using their phone number",
        request_body=UserForgetPassSerializer,
        responses={200: "sms sent", 400: "error message"}
    )
    def post(self, request):
        ser_data = UserForgetPassSerializer(data=request.data)

        if ser_data.is_valid():
            user = User.objects.get(phone_number=ser_data.validated_data['phone_number'])
            random_code = random.randint(1000, 9999)
            user.random_code = random_code
            user.save()

            conn = http.client.HTTPSConnection("api.sms.ir")

            payload = {
                "mobile": f"{user.phone_number}",
                "templateId": 100000,
                "parameters": [
                    {
                        "name": "PARAMETER1",
                        "value": "000000"
                    },
                    {
                        "name": "CODE",
                        "value": f"{user.random_code}"
                    }
                ]
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'text/plain',
                'x-api-key': 'OWset3DJhlMJVwmqiuXXEiFfqHhHtxzdIMETGnmgEO94wOCFe19p2f6gZExmX7HU'
            }
            json_payload = json.dumps(payload).encode('utf-8')
            conn.request("POST", "/v1/send/verify", json_payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

            return Response({'detail': 'sms sent'}, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint is used to verify the entered code for user's password reset request",
        request_body=UserRandomCodeSerializer,
        responses={200: "code matched", 406: "code doesnt matched", 400: "error message"}
    )
    def post(self, request, phone):
        ser_data = UserRandomCodeSerializer(data=request.data)

        if ser_data.is_valid():
            user = User.objects.get(phone_number=phone)
            print(type(user.random_code))
            print(type(ser_data.validated_data['code']))
            if user and user.random_code == int(ser_data.validated_data['code']):
                return Response({'detail': 'code matched'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'code doesnt matched'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint is used to reset user password",
        request_body=UserChangePasswordSerializer,
        responses={200: "password changed", 400: "error message"}
    )
    def post(self, request, phone):
        ser_data = UserChangePasswordSerializer(data=request.data)

        if ser_data.is_valid():
            user = User.objects.get(phone_number=phone)

            if user:
                user.set_password(ser_data.validated_data['password1'])
                user.save()
                return Response({'detail': 'password changed'}, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
