from django.urls import path

from .views import UserListAPIView, UserDetailAPIView, RegisterUserView, OTPVerifyUser

app_name = 'api-user'

urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='signup'),
    path('', UserListAPIView.as_view(), name='list'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='detail'),
    path('verify/', OTPVerifyUser.as_view(), name='verify-user')
]