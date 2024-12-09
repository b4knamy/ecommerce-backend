from django.db import models
from django.utils.translation import gettext_lazy as _

from core.settings.site import FILE_UPLOAD_MAX_MEMORY_SIZE_MB, MAX_COMMENT_PER_PAGE, MAX_FILE_PER_COMMENT, MAX_GLASSES_PER_PAGE, MAX_SEARCH_PRODUCT_PER_PAGE


class APIConfigs(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("API Name"))
    url = models.CharField(max_length=150, verbose_name=_("Endereço da API"))
    reference = models.CharField(
        max_length=50, verbose_name=_("API Reference"), blank=True)

    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    external_domain = models.CharField(
        max_length=100, verbose_name=_("Dominio do site externo"), blank=True)
    site_name = models.CharField(
        max_length=100, verbose_name=_("Nome do site"))
    site_domain = models.CharField(max_length=100, verbose_name=_("Dominio"))

    max_image_size = models.IntegerField(
        verbose_name=_("Tamanho maximo de arquivos (MB)"), default=FILE_UPLOAD_MAX_MEMORY_SIZE_MB)
    max_file_per_comment = models.IntegerField(
        verbose_name=_("Tamanho maximo de arquivos permitido por comentário"), default=MAX_FILE_PER_COMMENT)
    max_product_pagination = models.IntegerField(
        verbose_name=_("Tamanho maximo de produtos por pesquisa (Paginação)"), default=MAX_GLASSES_PER_PAGE)
    max_comments_pagination = models.IntegerField(
        verbose_name=_("Tamanho maximo de comentários (Paginação)"), default=MAX_COMMENT_PER_PAGE)
    max_product_query_pagination = models.IntegerField(
        verbose_name=_("Tamanho maximo maximo de produtos por pesquisa dinamica (Paginação)"), default=MAX_SEARCH_PRODUCT_PER_PAGE)
    default_image_url = models.CharField(max_length=150, verbose_name=_(
        "Imagem padrão para quando produto não possui imagem"))

    filter_1 = models.CharField(
        max_length=30, verbose_name=_("Nome de filtro 1"), blank=True)
    param_1 = models.CharField(
        max_length=30, verbose_name=_("Parametro de pesquisa 1"), blank=True)

    filter_2 = models.CharField(
        max_length=30, verbose_name=_("Nome de filtro 2"), blank=True)
    param_2 = models.CharField(
        max_length=30, verbose_name=_("Parametro de pesquisa 2"), blank=True)

    filter_3 = models.CharField(
        max_length=30, verbose_name=_("Nome de filtro 3"), blank=True)
    param_3 = models.CharField(
        max_length=30, verbose_name=_("Parametro de pesquisa 3"), blank=True)

    filter_4 = models.CharField(
        max_length=30, verbose_name=_("Nome de filtro 4"), blank=True)
    param_4 = models.CharField(
        max_length=30, verbose_name=_("Parametro de pesquisa 4"), blank=True)

    filter_5 = models.CharField(
        max_length=30, verbose_name=_("Nome de filtro 5"), blank=True)
    param_5 = models.CharField(
        max_length=30, verbose_name=_("Parametro de pesquisa 5"), blank=True)

    filter_6 = models.CharField(
        max_length=30, verbose_name=_("Nome de filtro 6"), blank=True)
    param_6 = models.CharField(
        max_length=30, verbose_name=_("Parametro de pesquisa 6"), blank=True)

    def __str__(self):
        return "Configuração do site"
