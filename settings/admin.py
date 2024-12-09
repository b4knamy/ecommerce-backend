from django.contrib import admin

from .models import APIConfigs, SiteSettings

# Register your models here.


@admin.register(APIConfigs)
class APIConfigsAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    pass
