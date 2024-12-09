from .models import SiteSettings
from rest_framework.serializers import ModelSerializer


class SiteSettingsSerializer(ModelSerializer):

    class Meta:
        model = SiteSettings
        fields = "__all__"
