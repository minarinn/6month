from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "first_name", "last_name", "registration_source", "is_active", "is_staff")
    ordering = ("email",)
    list_filter = ("registration_source", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "phone_number", "birthdate")}),
        ("Метаданные", {"fields": ("registration_source", "last_login")}),
        ("Статусы", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "is_active", "is_staff"),
        }),
    )
    
    readonly_fields = ("last_login",)