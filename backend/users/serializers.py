from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User
from core.serializers import Base64ImageField


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,)
    email = serializers.EmailField(required=True,)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]

    def validate_password(self, value):
        user = self.context['request'].user
        try:
            validate_password(value, user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже зарегистрирован."
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже зарегистрирован."
            )
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))


class UserDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(max_size=5 * 1024 * 1024)

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.subscriber.filter(
                subscribed_on=obj
            ).exists()
        return False


class UserAvatarSerializer(serializers.ModelSerializer):

    avatar = Base64ImageField(
        max_size=5 * 1024 * 1024, required=True,
    )

    class Meta:
        model = User
        fields = [
            'avatar',
        ]


class UserSetPasswordSerializer(serializers.ModelSerializer):

    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'current_password',
            'new_password',
        ]

    def validate(self, data):
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError(
                {"detail": "Пароли не могут совпадать."}
            )
        return data

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.email, password=value):
            raise serializers.ValidationError("Текущий пароль неверный.")
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        try:
            validate_password(value, user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
