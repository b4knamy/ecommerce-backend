# Generated by Django 5.0.6 on 2024-12-13 08:16

import django.contrib.auth.password_validation
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('reset_code', models.CharField(max_length=6)),
                ('expiration', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('edited_at', models.DateTimeField(auto_now=True, verbose_name='Data da ultima edição')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='Identificador')),
                ('first_name', models.CharField(blank=True, max_length=150, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='last name')),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator('^(?=.*[A-Za-z])(?=.*\\d)(?=.*[!@#$%&_])[A-Za-z\\d!@#$%&_]+$', 'A senha precisa conter no mínimo: um numero, uma letra minuscula, maiuscula e um caractere especial.'), django.contrib.auth.password_validation.validate_password], verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Endereço')),
                ('complement', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('zipcode', models.CharField(blank=True, max_length=12, null=True, verbose_name='CEP')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'ordering': ['email'],
            },
        ),
    ]
