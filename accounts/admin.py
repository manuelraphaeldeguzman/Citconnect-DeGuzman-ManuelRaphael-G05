from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as userAdmin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = userAdmin.fieldsets + (
        ("School Profile", {'fields': ('role', 'course')}),
    )