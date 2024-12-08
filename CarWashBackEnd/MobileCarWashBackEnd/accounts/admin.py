from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm, WorkerUserCreationForm, WorkerUserChangeForm
from .models import User, WorkerUser, CustomerUser


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'phone_number','is_worker' ,'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'gender','password', 'random_code')}),
        ('Permissions', {'fields': ('is_active', 'is_worker','is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'first_name', 'last_name', 'gender','password1', 'password2'),}),
    )


    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name')

    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)   



class WorkerUserAdmin(BaseUserAdmin):
    form = WorkerUserChangeForm
    add_form = WorkerUserCreationForm
    list_display = ('email', 'phone_number')
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'gender', 'is_available', 'password', 'random_code')}),
        ('Permissions', {'fields': ('is_active','is_admin', 'is_worker', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'gender','workerID', 'first_name', 'last_name', 'password1', 'password2'),}),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ()

    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(WorkerUser, WorkerUserAdmin)   


class CustomerUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'phone_number')
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'gender', 'password', 'random_code')}),
        ('Permissions', {'fields': ('is_active', 'is_worker','is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number','gender', 'email', 'password1', 'password2'),}),
    )


    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name')

    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(CustomerUser, CustomerUserAdmin)  

