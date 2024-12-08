from django.urls import path
from . import views

app_name= 'services'

urlpatterns = [
    path('', views.ServicesView.as_view(), name='services_page'),
    path('<slug:slug>/', views.ServicesDetailView.as_view(), name='service_detail')
]