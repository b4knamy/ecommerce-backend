from django.urls import path
from .views import (
    UserProfileView, get_csrf_token, CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView, CreateUserView,
    create_reset_code, change_password
)
from authentication.views import SimpleUserView
from rest_framework_simplejwt.views import TokenVerifyView

app_name = 'authentication'
urlpatterns = [
    path("user/create", CreateUserView.as_view(), name="CreateUserView"),

    path("user/data", SimpleUserView.as_view(), name="simple-user-view"),

    path('token', CookieTokenObtainPairView.as_view(),
         name='cookie_token_obtain_pair'),

    path('token/refresh', CookieTokenRefreshView.as_view(),
         name='cookie_token_refresh'),

    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    path('token/logout', LogoutView.as_view(), name="logout_view"),


    # APIS CSRF TOKEN
    path("csrftoken", view=get_csrf_token, name="get_csrf_token"),

    path("profile/user/<str:slug>", view=UserProfileView.as_view(), name="user_profile_view"),

    path("user/password/reset_code", view=create_reset_code, name="create_reset_code"),
    path("user/password/change", view=change_password, name="change_password"),
]
