from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Orders
from services.models import Services, Comment
from accounts.models import CustomerUser, WorkerUser

from .serializer import OrdersCreateSerializer, OrderChangeSerializer, AddCommentSerializer



class OrderCreateView(APIView):
        permission_classes=[IsAuthenticated,]

        @swagger_auto_schema(
            operation_description="This endpoint is used to create a new order "
                                  " \nworker filed must be empty "
                                  " \npermission -> only authenticated user can access this endpoint",
            request_body=OrdersCreateSerializer,
            responses={201: "order created", 400: "error message", 401: "Unauthorized"}
        )
        def post(self, request, slug):
                service = Services.objects.get(slug=slug)
                user = CustomerUser.objects.get(email=request.user)
                ser_data = OrdersCreateSerializer(data=request.data, context={'service': service})

                if ser_data.is_valid():
                        Orders.objects.create(customer=user,
                                              service=service,
                                              car_type=ser_data.validated_data['car_type'],
                                              address=ser_data.validated_data['address'],
                                              time=ser_data.validated_data['time'])
                        return Response({'detail': 'order created'}, status=status.HTTP_201_CREATED)
                
                return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                        

                
class OrderPayView(APIView):
    permission_classes=[IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="This endpoint is used to pay an order "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "order paid", 401: "Unauthorized"}
    )

    def put(self, request, order_id):
        order = Orders.objects.get(id=order_id)
        order.is_paid = True
        order.status = 'waiting'
        order.save()
        return Response({'detail': 'order paid'}, status=status.HTTP_200_OK)
    
   

class PickWorkerOrderView(APIView):
    permission_classes=[IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="This endpoint is used pick a worker for order by admin "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "worker picked", 401: "Unauthorized", 403: "access denied"}
    )
    def put(self, request, order_id, worker_id):
        if request.user.is_admin:
            order = Orders.objects.get(id=order_id)
            worker = WorkerUser.objects.get(email=worker_id)
            order.worker = worker
            order.status = 'in_progress'
            order.save()
            worker.is_available = False
            worker.save()
            return Response({'detail': 'worker picked'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
    


class ChangeWorkerStatusView(APIView):
    permission_classes=[IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="This endpoint allows workers to change their status "
                              " \nonly fill 'worker_status' field "
                              " \npermission -> only authenticated user can access this endpoint",
        request_body=OrderChangeSerializer,
        responses={200: "worker status changed", 401: "Unauthorized", 403: "access denied"}
    )
    def put(self, request, order_id):
        if request.user.is_worker:
            order = Orders.objects.get(id=order_id)
            ser_data = OrderChangeSerializer(instance=order, data=request.data, partial = True)
            if ser_data.is_valid():
                 order.worker_status = ser_data.validated_data['worker_status']
                 order.save()
                 return Response({'detail': 'worker status changed'}, status=status.HTTP_200_OK)

        return Response({'detail': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
              
     
        
    
class CancelOrderView(APIView):
    permission_classes=[IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="This endpoint allows workers to cancel their orders "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "order canceled", 401: "Unauthorized", 403: "access denied"}
    )
    def put(self, request, order_id):
        if request.user.is_worker: 
            order = Orders.objects.get(id=order_id)
            order.worker = None
            order.worker_status = None
            order.status = 'waiting'
            worker = WorkerUser.objects.get(email=request.user)
            worker.is_available = True
            worker.save()
            order.save()
            return Response({'detail': 'order canceled'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
    

class FinishOrderView(APIView):
    permission_classes=[IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="This endpoint allows workers to finish their orders "
                              " \npermission -> only authenticated user can access this endpoint",
        responses={200: "order finished", 401: "Unauthorized", 403: "access denied"}
    )
    def put(self, request, order_id):
        if request.user.is_worker: 
            order = Orders.objects.get(id=order_id)
            order.worker_status = None
            order.status = 'finished'
            worker = WorkerUser.objects.get(email=request.user)
            worker.is_available = True
            worker.save()
            order.save()
            return Response({'detail': 'order finished'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'access denied'}, status=status.HTTP_403_FORBIDDEN)
            

class AddCommentView(APIView):
    permission_classes=[IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="This endpoint allows customers to add a comment below orders "
                              " \nonly fill 'body' field "
                              " \npermission -> only authenticated user can access this endpoint",
        request_body=AddCommentSerializer,
        responses={201: "comment posted", 401: "Unauthorized", 400: "error message"}
    )
    def post(self, request, order_id):
        order = Orders.objects.get(id=order_id)

        if order.status == 'finished':
            user = CustomerUser.objects.get(email=request.user)
            ser_data = AddCommentSerializer(data=request.data)

            if ser_data.is_valid():
                Comment.objects.create(user=user,
                                        service=order.service,
                                        worker=order.worker,
                                        body=ser_data.validated_data['body'])
                return Response({'detail': 'comment posted'}, status=status.HTTP_201_CREATED)
                    
            return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

