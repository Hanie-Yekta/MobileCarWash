from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('wregister/', views.WorkerUserRegisterView.as_view(), name='wuser_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('worker_profile/', views.WorkerUserProfileView.as_view(), name='worker_profile'),
    path('admin_profile/', views.AdminUserProfileView.as_view(), name='admin_profile'),
    path('customer_profile/', views.CustomerUserProfileView.as_view(), name='customer_profile'),
    path('get_info/', views.GetUserInfo.as_view(), name='get_user_info'),
    path('forget_pass/', views.ForgetPasswordView.as_view(), name='forget_pass'),
    path('verify_code/<str:phone>/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('change_pass/<str:phone>/', views.UserChangePasswordView.as_view(), name='change_password'),
]