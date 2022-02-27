from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'username',) 


class UserProfileForm(forms.ModelForm):
     class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'username', 'first_name', 'last_name') 
