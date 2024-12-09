
from .utils import forms
from core.settings import (
    CLIENT_OWNER_SITE_DOMAIN,
    CLIENT_OWNER_SITE_HEADER,
    CLIENT_OWNER_SITE_TITLE
)
from django.contrib import admin
from .models import Brand, Category, Glasses, Model, Color,  Image, Shape
from .utils.admin_models.extra_models import ImageInTabular
from .utils.actions import (
    change_is_promo_to_true,
    change_is_promo_to_false,
    change_is_promo_and_is_sample_to_true,
    change_is_promo_and_is_sample_to_false,
    change_is_sample_to_true,
    change_is_sample_to_false,
)
from django.utils.translation import gettext_lazy as _


@admin.register(Glasses)
class GlassesAdmin(admin.ModelAdmin):
    form = forms.CustomAdminForm

    inlines = [ImageInTabular]
    list_filter = ["name", "is_promo", "is_sample"]
    readonly_fields = ("created_at", "edited_at", "slug", "installments_amount")
    list_display = ["name",  "gender", "amount",
                    "quantitaty", "is_sample", "is_promo"]
    search_fields = ("name",)
    search_help_text = _('Buscar Oculos pelo "Nome"')
    filter_horizontal = ("color", "brand", "category", "model", "shape")
    actions = (
        change_is_promo_to_true,
        change_is_promo_to_false,
        change_is_sample_to_true,
        change_is_sample_to_false,
        change_is_promo_and_is_sample_to_true,
        change_is_promo_and_is_sample_to_false,)
    fieldsets = (
        (None, {
            "fields": (
                "name",
            ),
        }),
        (
            "Caracteristicas", {
                "fields": (
                    "category", "color", "model", "shape", "brand"
                )
            }
        ),
        ("Pagamentos", {"fields": ("amount", "installments_amount",
         "installments_count", "discount", "is_promo")}),
        ("Outras informações", {"fields": ("is_sample", "quantitaty", "temple", "rim",
         "nose_pads", "bridge", "width", "height", "warranty", "description")}),
        ("Não editáveis", {
            "fields": (
                "slug", "created_at", "edited_at",
            )
        }),

    )


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    search_help_text = _('Buscar pela Formato')
    readonly_fields = ("slug",)
    form = forms.CustomAdminForm


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    search_help_text = _('Buscar pela Marca')
    readonly_fields = ("slug",)
    form = forms.CustomAdminForm


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ("description",)
    search_help_text = _('Buscar pela descrição da Imagem')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)
    search_fields = ("name",)
    search_help_text = _('Buscar pela Categoria')
    form = forms.CustomAdminForm


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)
    search_fields = ("name",)
    search_help_text = _('Buscar pela Cor')
    form = forms.CustomAdminForm


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)
    form = forms.CustomAdminForm
    search_fields = ("name",)
    search_help_text = _('Buscar pelo Modelo')


admin.site.site_header = CLIENT_OWNER_SITE_HEADER
admin.site.index_title = _('Área de configuração')
admin.site.site_title = CLIENT_OWNER_SITE_TITLE
admin.site.site_url = CLIENT_OWNER_SITE_DOMAIN
