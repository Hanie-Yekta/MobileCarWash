from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import WorkerUser, CustomerUser, User



STATIC_WORKER_ID = 355

def clean_email(value):
        user = User.objects.filter(email=value).exists()
        if user:
            raise ValidationError('این ایمیل قبلا ثبت شده است.')
        return value


def clean_phone(value):
        user=User.objects.filter(phone_number=value).exists()
        if user:
            raise ValidationError('این شماره تلفن قبلا ثبت شده است.')
        return value

def clean_WID(value):
    if value != STATIC_WORKER_ID:
         raise ValidationError('شناسه وارد شده اشتباه است.')
    return value



#register
class WorkerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'gender', 'workerID', 'password', 'is_admin', 'is_worker')
        extra_kwargs = {
            'email' : {'validators': (clean_email,)},
            'phone_number' : {'validators': (clean_phone,)},
            'workerID' : {'validators': (clean_WID,)},
            'password':{'write_only':True}
        }



class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'gender', 'password', 'is_admin', 'is_worker')
        extra_kwargs = {
            'email' : {'validators': (clean_email,)},
            'phone_number' : {'validators': (clean_phone,)},
            'password':{'write_only':True}
        }



class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'gender', 'password', 'is_admin', 'is_worker')
        extra_kwargs = {
            'email' : {'validators': (clean_email,)},
            'phone_number' : {'validators': (clean_phone,)},
            'password':{'write_only':True}
        }



class UserForgetPassSerializer(serializers.Serializer):
     phone_number = serializers.CharField(max_length=11)



class UserRandomCodeSerializer(serializers.Serializer):
     code = serializers.CharField(max_length=4)


class UserChangePasswordSerializer(serializers.Serializer):
     password1=serializers.CharField()
     password2=serializers.CharField()