
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from authentication.models import PasswordReset, User
from rest_framework.decorators import permission_classes, authentication_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
import logging
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from utils.utils import error_response
from .serializers import (
    CreateUserSerializer,
    UserPasswordSerializer,
    SimpleUserSerializer,
    UserProfileSerializer,
    CookieTokenRefreshSerializer,
    CookieTokenObtainPairViewSerializer
)


logger = logging.getLogger("debugger")


class SimpleUserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):

        user = request.user
        serializer = SimpleUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer


@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    answer = JsonResponse(data={"csrf_token": token})
    answer.set_cookie('csrf_token', token, httponly=True,
                      secure=False, samesite='Lax')
    return answer


class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CookieTokenObtainPairViewSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            print(response.data)
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        requested_user = get_object_or_404(User, slug=slug)

        if self.is_current_user(request.user, requested_user):

            try:
                user_profile_serializer = UserProfileSerializer(requested_user)
                return Response(user_profile_serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, slug):
        requested_user = get_object_or_404(User, slug=slug)

        if self.is_current_user(request.user, requested_user):

            self.update_user_data(request, request.user)
            return Response({"slug": request.user.slug}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, slug):
        if request.user.slug == slug:
            user = User.objects.get(slug=slug)
            user.delete()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def is_current_user(self, first_user: User, second_user: User) -> bool:
        return first_user == second_user

    def update_user_data(self, request, user: User):
        serializer = UserProfileSerializer(
            user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def create_reset_code(request):

    user = request.user
    if olders_pwd_reset := PasswordReset.objects.filter(email=user.email):
        for pwr in olders_pwd_reset:
            pwr.delete()

    password_code = PasswordReset.objects.create(email=user.email)
    password_code.save()
    password_code.send_reset_code()
    # sleep(3)

    return Response(status=status.HTTP_200_OK)

# TODO: make the code be delete after 15 min if possible.


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def change_password(request):

    user: User = request.user
    password_code = get_object_or_404(PasswordReset, email=user.email)

    if password_code.is_reset_code_expired:
        return error_response("Codigo de verificação expirado.", key="reset_code")

    reset_code = request.data.get("reset_code")

    if not password_code.is_reset_code_checked(reset_code):
        return error_response("Codigo de verificação está incorreto.", key="reset_code")

    user_pwd_serializer = UserPasswordSerializer(user,
                                                 data=request.data, partial=True, context={"user": user})

    if user_pwd_serializer.is_valid(raise_exception=True):
        user_pwd_serializer.save()
        password_code.send_confirm_password_change()
        password_code.delete()
        return Response({"success": _("Senha alterada com sucesso!")}, status=status.HTTP_200_OK)
