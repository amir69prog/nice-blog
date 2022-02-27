from django.urls import path

from .views import user_profile_view, SignupView

app_name = 'accounts'
urlpatterns = [
    path('profile/', user_profile_view, name='profile'),
    path('signup/', SignupView.as_view(), name='signup')
]