from datetime import timedelta
from random import randint
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password


from django.utils.translation import gettext_lazy as _
from data.models import AbstractModel
from django.utils import timezone
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, AbstractModel):
    first_name = models.CharField(
        _("first name"), max_length=150, blank=True, validators=[MinLengthValidator(3)])
    last_name = models.CharField(
        _("last name"), max_length=150, blank=True, validators=[MinLengthValidator(3)])

    PASSWORD_VALITADOR = RegexValidator(
        r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%&_])[A-Za-z\d!@#$%&_]+$',
        _("A senha precisa conter no mínimo: um numero, uma letra minuscula, maiuscula e um caractere especial."))
    username = None
    date_joined = None
    password = models.CharField(_("password"), max_length=128,
                                validators=[PASSWORD_VALITADOR, validate_password])

    email = models.EmailField(_("Email"), unique=True)
    # is_superuser = models.BooleanField(
    #     _("Admin"),
    #     default=False,
    #     help_text=_(
    #         "Designates that this user has all permissions without "
    #         "explicitly assigning them."
    #     ),
    # )
    address = models.CharField(_("Endereço"), max_length=200, null=True, blank=True)
    complement = models.CharField(
        _("Complemento"), max_length=100, null=True, blank=True)
    zipcode = models.CharField(_("CEP"), max_length=12, null=True, blank=True)
    objects = CustomUserManager()

    ADMIN_SITE_WELCOME_NAME = "first_name"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} - {self.email}"

    def delete(self, *args, **kwargs):

        # if self.comments_user:
        #     print("EXCLUDE COMMENTS FROM USER")
        #     for comment in self.comments.all():
        #         comment.delete()

        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # if len(self.first_name) < 2 or len(self.last_name) < 2:
        #     raise ValidationError(_("O campo precisa ter no minimo 2 caracteres."))

        return super().save(*args, **kwargs)

    @property
    def default_slug_name(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["email"]


class PasswordReset(models.Model):
    email = models.EmailField(_("Email"), unique=True)
    reset_code = models.CharField(max_length=6)
    expiration = models.DateTimeField()

    @property
    def is_reset_code_expired(self):
        return timezone.now() > self.expiration

    def save(self, *args, **kwargs):
        self.reset_code = str(randint(100000, 999999))
        self.expiration = timezone.now() + timedelta(minutes=15)
        return super().save(*args, **kwargs)

    def send_reset_code(self):
        send_mail(
            subject="Password Reset",
            message=_(f"Your reset code to change your password are: {
                      self.reset_code}"),
            recipient_list=[self.email],
            from_email=None
        )

        # TODO: make a html user friendly page

    def send_confirm_password_change(self):
        send_mail(
            subject="Password Reset - Changed",
            message=_(f"Your password was changed successfully."),
            recipient_list=[self.email],
            from_email=None
        )

    def is_reset_code_checked(self, reset_code):
        return self.reset_code == reset_code
