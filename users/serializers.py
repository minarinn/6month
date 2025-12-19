from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    birthdate = serializers.DateField(required=False, allow_null=True)
    
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('Пользователь с таким email уже существует!')


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = str(user.birthdate) if user.birthdate else None
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token


class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()