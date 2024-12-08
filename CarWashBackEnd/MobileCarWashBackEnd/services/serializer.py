from rest_framework import serializers
from .models import Services, ServicePrice, Comment
from accounts.serializer import WorkerUserSerializer, CustomerUserSerializer

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('id', 'image', 'name', 'slug',)


class DetailServiceSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='get_prices')
    comment = serializers.SerializerMethodField(method_name='get_comment')

    class Meta:
        model = Services
        fields = ('__all__')


    def get_prices(self, obj):
        result = obj.prices.all()
        return PriceServiceSerializer(instance=result, many=True).data
    
    def get_comment(self, obj):
        result = obj.scomments.all()
        return CommentServiceSerializer(instance=result, many=True).data



class PriceServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePrice
        fields = ('__all__')


class CommentServiceSerializer(serializers.ModelSerializer):
    user = CustomerUserSerializer()
    worker = WorkerUserSerializer()
    class Meta:
        model = Comment
        fields = ('__all__')


