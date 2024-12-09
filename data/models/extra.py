from data.models import AbstractExtraModels
from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(AbstractExtraModels):
    def get_name_verbose_name(self):
        return _("Marca")

    class Meta:

        verbose_name = _("Marca")
        verbose_name_plural = _("Marcas")


class Category(AbstractExtraModels):
    def get_name_verbose_name(self):
        return _("Categoria")

    class Meta:

        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


class Color(AbstractExtraModels):
    css_color = models.CharField(_("Valor RGB"), max_length=40, help_text=_(
        "Esse campo será usado para identificar a cor"), blank=True)

    def get_name_verbose_name(self):
        return _("Cor")

    class Meta:

        verbose_name = _("Cor")
        verbose_name_plural = _("Cores")


class Shape(AbstractExtraModels):
    def get_name_verbose_name(self):
        return _("Formato")

    class Meta:

        verbose_name = _("Formato")
        verbose_name_plural = _("Formatos")


class Model(AbstractExtraModels):

    def get_name_verbose_name(self):
        return _("Modelo")

    class Meta:
        verbose_name = _("Modelo")
        verbose_name_plural = _("Modelos")
