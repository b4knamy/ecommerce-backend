from rest_framework import serializers

from payment.serializers import PaymentOrderSerializer
from .models import User
from django.core.validators import RegexValidator
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import default_user_authentication_rule
from rest_framework_simplejwt.settings import api_settings
from django.core.validators import MinLengthValidator


class CreateUserSerializer(serializers.Serializer):
    password_validator = RegexValidator(
        r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
        "A senha precisa conter no mínimo: um numero, uma letra minuscula, maiuscula e um caractere especial.")
    password = serializers.CharField(
        max_length=128, min_length=8, validators=[password_validator])
    first_name = serializers.CharField(
        max_length=60, validators=[MinLengthValidator(3)])
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Esse endereço de email já existe.")

        return value

    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Este campo é obrigátorio.")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id", "email", "first_name", "last_name", "slug"]


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie \'refresh_token\'')


class CookieTokenObtainPairViewSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """
        THIS FUNCTION WAS OVERHIDDEN TO IMPLEMENT A CUSTOM ERROR MESSAGE
        WHEN AN USER EXISTS AND IS NOT ACTIVE (BANISHED)
        AND I SAW SOME USELESS CALLS BY INHERITANCE AND I IMPLEMENTED
        THE VALIDATION AND SERIALIZATION AT THE SAME FUNCTION.
        THIS FUNCTION WAS CALLING SUPER().VALIDATE(ATTRS)
        WHICH IS RETURNING {}.
        """

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        try:
            check_user = User.objects.get(email=authenticate_kwargs["email"])
            if not check_user.is_active:
                raise AuthenticationFailed(
                    "Esta conta foi banida por tempo indeterminado!",
                    code='user_is_banished'
                )
        except User.DoesNotExist:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not default_user_authentication_rule(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)
        data = {}

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    payment_orders = PaymentOrderSerializer(many=True, required=True)

    class Meta:

        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "address",
            "complement",
            "zipcode",
            "payment_orders",
            "slug",
        )


class UserPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        max_length=128, required=True, write_only=True)

    class Meta:

        model = User

        fields = ("password", "current_password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        old_pwd = attrs["current_password"]
        new_pwd = attrs["password"]
        user: User = self.context["user"]

        if not user.check_password(old_pwd):
            raise serializers.ValidationError(_("Senha atual está incorreta."))

        if user.check_password(new_pwd):
            raise serializers.ValidationError(
                _("A nova senha não pode ser igual a atual."))

        return attrs

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance
