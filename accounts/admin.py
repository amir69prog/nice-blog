from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomAdminUser(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_verified')}),
    )
    list_display = ('phone_number', 'username', 'email',
                    'is_verified', 'is_superuser',)


admin.site.register(CustomUser, CustomAdminUser)
