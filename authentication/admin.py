from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import User
from .utils.actions import (
    change_user_is_active_to_true,
    change_user_is_active_to_false,
    change_user_is_staff_to_true,
    change_user_is_staff_to_false,
    change_user_is_superuser_to_true,
    change_user_is_superuser_to_false,
)


@admin.register(User)
class AdminUser(UserAdmin):
    list_filter = ["email", "is_staff", "is_active", "is_superuser"]
    list_display = ["email", "first_name", "last_name",
                    "is_superuser", "is_staff", "is_active"]
    search_fields = ("email",)
    search_help_text = _('Buscar por "Email"')
    actions = (
        change_user_is_active_to_true,
        change_user_is_active_to_false,
        change_user_is_staff_to_true,
        change_user_is_staff_to_false,
        change_user_is_superuser_to_true,
        change_user_is_superuser_to_false,
    )
    ordering = ("email",)
    fieldsets = (
        (_("Personal info"), {
            "fields": ("email", "first_name", "last_name", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {
            "fields": ("last_login", "created_at")}),
    )
    readonly_fields = ("created_at", "last_login")
