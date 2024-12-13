from rest_framework.decorators import api_view
from settings.serializers import SiteSettingsSerializer
from .models import APIConfigs, SiteSettings
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

# Create your views here.


@cache_page(60 * 60 * 1)
@api_view(["GET"])
def site_configs(request):
    urls = {}
    site_settings = SiteSettings.objects.first()
    domain = site_settings.site_domain

    for url in APIConfigs.objects.all():
        urls[url.name] = f"{domain}/{url.url}"

    settings_serializer = SiteSettingsSerializer(site_settings)

    response = {
        "api": urls,
        "settings": settings_serializer.data,
    }
    return Response(response, 200)
