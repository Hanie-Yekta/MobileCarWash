from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('<slug:slug>/', views.OrderCreateView.as_view(), name='order_creat'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('order_detail/<int:order_id>/<str:worker_id>/', views.PickWorkerOrderView.as_view(), name='pick_worker'),
    path('cancel/<int:order_id>/', views.CancelOrderView.as_view(), name='cancel'),
    path('finish/<int:order_id>/', views.FinishOrderView.as_view(), name='finish'),
    path('change_wstatus/<int:order_id>/', views.ChangeWorkerStatusView.as_view(), name='change_worker_status'),
    path('comment/<int:order_id>/', views.AddCommentView.as_view(), name='add_comment'),

]