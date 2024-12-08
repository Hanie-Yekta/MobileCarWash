from django.db import models
from accounts.models import CustomerUser, WorkerUser
from services.models import Services, ServicePrice


# Create your models here.


class Orders(models.Model):
    W = 'waiting'
    P = 'in_progress'
    F = 'finished'

    I = 'in_way'
    D = 'doing'

    SERVICE_STATUS = [
        (W , 'waiting'),
        (P , 'in_progress'),
        (F , 'finished'),
    ]



    WORKER_STATUS = [
        (I , 'in_way'),
        (D , 'doing'),
    ]

    

    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='cu_order')
    worker = models.ForeignKey(WorkerUser, on_delete=models.CASCADE, related_name='wo_order', blank=True, null=True)
    worker_status = models.CharField(choices=WORKER_STATUS, blank=True, null=True, max_length=10)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='serv_order')
    car_type = models.CharField(max_length=20, choices=ServicePrice.CAR_TYPES, blank=True, null=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True)
    time = models.TimeField()
    status = models.CharField(choices=SERVICE_STATUS, blank=True, null=True, max_length=15)
    is_paid = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.car_type and self.service:
            try:
                service_price = ServicePrice.objects.get(service=self.service, car_type=self.car_type)
                self.price = service_price.price
            except ServicePrice.DoesNotExist:
                self.price = None
        super().save(*args, **kwargs)
    
