from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.action(description=_("Ativar promoção em selecionados"))
def change_is_promo_to_true(modeladmin, request, queryset):
    queryset.update(is_promo=True)


@admin.action(description=_("Desativar promoção em selecionados"))
def change_is_promo_to_false(modeladmin, request, queryset):
    queryset.update(is_promo=False)


@admin.action(description=_('Ativar "Promoção" e "Inicio da pagina" em selecionados'))
def change_is_promo_and_is_sample_to_true(modeladmin, request, queryset):
    queryset.update(is_promo=True, is_sample=True)


@admin.action(description=_('Desativar "Promoção" e "Inicio da pagina" em selecionados'))
def change_is_promo_and_is_sample_to_false(modeladmin, request, queryset):
    queryset.update(is_promo=False, is_sample=False)


@admin.action(description=_("Ativar selecionados no inicio da pagina"))
def change_is_sample_to_true(modeladmin, request, queryset):
    queryset.update(is_sample=True)


@admin.action(description=_("Desativar selecionados no inicio da pagina"))
def change_is_sample_to_false(modeladmin, request, queryset):
    queryset.update(is_sample=False)
