
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def perform_slug_is_unique_error(field_value, field_name, obj):
    slug = slugify(field_value)
    instance = obj.objects.filter(slug=slug)
    if instance.exists():
        instance_field = getattr(instance.first(), field_name)
        if instance_field != field_value:
            msgError = f'O valor "{field_value}" cria um identificador "{
                slug}" já existente. Utilize outro valor.'
            msg = ValidationError(msgError, code="slug_must_be_unique")
            return msg

    return None


class CustomAdminForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        if name := cleaned_data.get("name", None):
            related_obj = self.instance.__class__
            if msg := perform_slug_is_unique_error(name, "name", related_obj):
                self.add_error("name", msg)
        return cleaned_data
