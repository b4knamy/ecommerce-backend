from django.contrib import admin
from data.models import Image


class ImageInTabular(admin.TabularInline):
    model = Image
    extra = 1
    fields = ("url", "description", "order")
