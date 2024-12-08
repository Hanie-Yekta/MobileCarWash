from django.contrib import admin
from .models import Orders

# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('customer', 'worker', 'service', 'time', 'address')

admin.site.register(Orders, OrdersAdmin)


