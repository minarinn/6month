from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    registration_source = models.CharField(
        max_length=20, 
        choices=[
            ('local', 'Local Registration'),
            ('google', 'Google OAuth'),
            ('facebook', 'Facebook OAuth'),
        ],
        default='local'
    )
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]
    
    def __str__(self) -> str:
        return self.email or ""
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='confirmation_code'
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Код подтверждения для {self.user.email}"
    
    class Meta:
        verbose_name = "Код подтверждения"
        verbose_name_plural = "Коды подтверждения"