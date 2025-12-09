from django.contrib import admin
from users.models import CustomUser, ConfirmationCode
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "phone_number", "is_active", "is_staff")
    ordering = ("email",)
    
    fieldsets = (
        (None, {"fields": ("email", "password", "phone_number")}),
        ("Статусы", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Важные даты", {"fields": ("last_login",)}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "password1", "password2", "is_active", "is_staff"),
        }),
    )

@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at")
    ordering = ("-created_at",)