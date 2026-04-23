from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('informações pessoais', {'fields': ('first_name', 'last_name')}),
        ('permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas importantes', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name')
        }),
    )

    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)