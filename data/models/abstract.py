from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class AbstractTimeStamp(models.Model):
    created_at = models.DateTimeField(
        auto_now=False, auto_now_add=True, verbose_name=_("Data de criação"))
    edited_at = models.DateTimeField(
        auto_now=True, auto_now_add=False, verbose_name=_("Data da ultima edição"))

    class Meta:
        abstract = True


class AbstractSlug(models.Model):
    slug = models.SlugField(unique=True, max_length=150,
                            verbose_name=_("Identificador"))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if not self.slug or self.is_slug_changed:
            self.slug = self.generate_unique_slug()

        return super().save(*args, **kwargs)

    def generate_unique_slug(self):
        default_slug_name = self.default_slug_name
        slug_name = slugify(default_slug_name)

        if self.__class__.__name__ == "User":
            while self.__class__.objects.filter(slug=slug_name).exists():
                slug_name = slugify(f"{default_slug_name}-{uuid4().hex[:6]}")
        else:
            if self.__class__.objects.filter(slug=slug_name).exists():
                raise ValueError(_(
                    f'O valor "{default_slug_name}" cria um identificador "{slug_name}" já existente. Utilize outro valor.'))

        return slug_name

    @property
    def is_slug_changed(self):
        old_instance = self.__class__.objects.filter(id=self.id).first()
        if old_instance:
            return self.slug != old_instance.slug or old_instance.default_slug_name != self.default_slug_name

    @property
    def default_slug_name(self):
        if not hasattr(self, "name") or not self.name:
            raise NotImplementedError(
                _('Atributo "name" não está implementado, crie ou sobreescreva referenciando outro atributo.'))
        return self.name


class AbstractModel(AbstractTimeStamp, AbstractSlug):

    class Meta:
        abstract = True


class AbstractExtraModels(AbstractSlug):

    def get_name_verbose_name(self):
        """This method must be implemented in subclasses for setting the verbose name of the name"""
        raise NotImplementedError(_('"get_name_verbose_name" must be implemented.'))

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("name").verbose_name = self.get_name_verbose_name()

    class Meta:
        abstract = True
        ordering = ["name"]
