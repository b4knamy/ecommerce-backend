from django.urls import path

from .views import site_configs

app_name = "settings"

urlpatterns = [
    path("site/settings", view=site_configs, name="site_settings"),
]
