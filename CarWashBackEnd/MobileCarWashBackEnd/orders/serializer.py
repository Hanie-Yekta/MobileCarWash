from rest_framework import serializers

from .models import Orders
from services.models import Comment

from accounts.serializer import CustomerUserSerializer, WorkerUserSerializer
from services.serializer import ServicesSerializer



class OrdersSerializer(serializers.ModelSerializer):
    customer = CustomerUserSerializer()
    worker = WorkerUserSerializer()
    service = ServicesSerializer()

    class Meta:
        model = Orders
        fields = ('__all__')






class OrdersCreateSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(read_only=True, slug_field='email')
    service = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Orders
        fields = ('customer', 'worker', 'service', 'car_type', 'address', 'time') 


    def validate_car_type(self, data):
        serv = self.context.get('service')
        if serv.slug == 'ceramic-coating-car' or serv.slug == 'engine-wash':
            if data != 'all_types':
                raise serializers.ValidationError("For this service, car_type must be 'all_types'.")
            
        else:
            if data == 'all_types':
                raise serializers.ValidationError("For this service, car_type cannot be 'all_types'.")

        return data




class OrderChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('__all__')


class AddCommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='email')
    service = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    
    class Meta:
        model = Comment
        fields = ('__all__')