from django.db import models
from django.urls import reverse

from accounts.models import CustomerUser, WorkerUser

# Create your models here.

class Services(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='services/')
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('services:service_detail', args=[self.slug,])
    

class ServicePrice(models.Model):
    SEDAN = 'sedan'
    HATCHBACK = 'hatchback'
    SUV = 'suv'
    ALL = 'all_types'

    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (HATCHBACK, 'Hatchback'),
        (SUV, 'SUV'),
        (ALL, 'all_types'),
    ]

    service = models.ForeignKey(Services, related_name='prices', on_delete=models.CASCADE)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, blank=True, null=True)
    price = models.PositiveIntegerField()

    def __str__(self):
            return f'{self.car_type}'
    


class Comment(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete = models.CASCADE, related_name = 'cucomments')
    service = models.ForeignKey(Services, on_delete = models.CASCADE, related_name = 'scomments')
    worker = models.ForeignKey(WorkerUser, on_delete=models.CASCADE, related_name='wocomments' , blank=True, null=True)
    body = models.TextField(max_length = 400)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'