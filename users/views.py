from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView

from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer
)
from users.models import CustomUser
from common.redis_utils import RedisConfirmationCode
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer


class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'Аккаунт пользователя не активирован!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'Неверные учетные данные!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data.get('phone_number', '')
        birthdate = serializer.validated_data.get('birthdate', None)

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            birthdate=birthdate,
            is_active=False
        )

        code = ''.join(random.choices(string.digits, k=6))
        
        RedisConfirmationCode.set_code(user.id, code, timeout=300)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code
            }
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'error': 'Пользователь не найден!'}
            )

        if not RedisConfirmationCode.verify_code(user_id, code):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Неверный или истёкший код подтверждения!'}
            )

        user.is_active = True
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'Аккаунт пользователя успешно активирован',
                'key': token.key
            }
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer