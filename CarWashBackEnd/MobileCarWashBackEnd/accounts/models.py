from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    F = 'female'
    M = 'male'

    GENDER = [
        (F , 'female'),
        (M , 'male'),
    ]

    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_worker = models.BooleanField(null=True, blank=True)
    random_code = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, blank=True, null=True, max_length=10)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number',]


    @property
    def is_staff(self):
        return self.is_admin
    

class WorkerUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='worker')
    workerID = models.IntegerField()
    is_available = models.BooleanField(default=True)



class CustomerUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')

