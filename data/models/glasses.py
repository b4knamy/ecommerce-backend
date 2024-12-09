from data.utils.validators import min_and_max_discount_value_validator
from django.utils.translation import gettext_lazy as _
from django.db import models
from data.models import AbstractModel, Category, Shape, Model, Color, Brand
from django.core.exceptions import ValidationError


class Glasses(AbstractModel):
    name = models.CharField(unique=True, max_length=200,
                            verbose_name=_("Nome"))
    category = models.ManyToManyField(
        Category, related_name="glasses_category", verbose_name=_("Categorias"))
    shape = models.ManyToManyField(
        Shape, related_name="glasses_shape", verbose_name=_("Formato"))
    model = models.ManyToManyField(
        Model, related_name="glasses_model", verbose_name=_("Modelo"))
    color = models.ManyToManyField(
        Color, related_name="glasses_color", verbose_name=_("Cor"))
    brand = models.ManyToManyField(
        Brand, related_name="glasses_brand", verbose_name=_("Marca"))
    material = models.CharField(
        max_length=50, verbose_name=_("Material do Óculos"))
    quantitaty = models.IntegerField(default=0, verbose_name=_("Quantidade"))

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Preço"))
    installments_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Preço de parcelamento"))
    installments_count = models.IntegerField(
        verbose_name=_("Quantidade de parcelas"))
    discount = models.IntegerField(verbose_name=_(
        'Desconto (Porcentagem)'), validators=[min_and_max_discount_value_validator,], default=0)

    gender = models.CharField(max_length=20, choices={
        'M': 'Masculino',
        'F': 'Feminino',
        'U': 'Unissex'
    }, verbose_name=_("Gênero"))
    is_sample = models.BooleanField(
        default=False, blank=True, verbose_name=_("Listar no inicio da página?"), help_text=_("Indica que o produto estará na pagina principal como recomendação."))
    is_promo = models.BooleanField(
        default=False, verbose_name=_("Está em promoção?"))
    slug = models.SlugField(unique=True, null=False, max_length=240, help_text=_(
        "Este campo é gerado automaticamente. É usado para identificação nos campos de buscas e filtragem. Deve ser único."))

    bridge = models.CharField(
        max_length=30, verbose_name=_("Ponte"))
    nose_pads = models.CharField(max_length=50,
                                 verbose_name=_("Protetor de nariz"))
    temple = models.CharField(max_length=30, verbose_name=_(
        "Hastes"))
    rim = models.CharField(max_length=30, verbose_name=_(
        "Aro"))
    description = models.TextField(
        max_length=800, verbose_name=_("Descrição"))
    width = models.CharField(max_length=30, verbose_name=_(
        "Largura"))
    height = models.CharField(max_length=30, verbose_name=_(
        "Altura"))
    warranty = models.CharField(
        max_length=20, verbose_name=_("Tempo de garantia"))

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):

        self.image.delete()

        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.installments_amount and self.installments_count:
            self.installments_amount = self.final_amount / self.installments_count

        return super().save(*args, **kwargs)

    @property
    def final_amount(self):
        if self.is_promo:
            return round(self.amount - ((self.amount * self.discount) / 100), 2)
        return self.amount

    def clean(self):
        super().clean()
        if self.is_promo and (self.discount is None or self.discount <= 0):
            raise ValidationError(
                _("Ao ativar uma promoção, é obrigatório especificar um valor de desconto."))

        if not self.is_promo and self.discount:
            raise ValidationError(
                _("Não é possivel adicionar um desconto sem ativar promoção."))

    class Meta:

        verbose_name = _("Óculos")
        verbose_name_plural = _("Óculos")
        ordering = ["name"]


class Image(models.Model):
    def create_image_path(self, file):
        return f"""oculos/{self.glasses.slug}/{file}"""

    glasses = models.ForeignKey(Glasses, verbose_name=_("Oculos"),
                                related_name="images", on_delete=models.CASCADE)
    url = models.ImageField(
        blank=True, upload_to=create_image_path, max_length=150, verbose_name=_("Imagem"))
    description = models.CharField(max_length=150, verbose_name=_("Descrição"))
    order = models.PositiveIntegerField(
        verbose_name=_("Ordem de exibição"), help_text=_("Ordem de exibição das imagens"))

    def delete(self, *args, **kwargs):

        self.url.delete(save=False)
        # for comment in self.comments.all():
        #     comment.delete()

        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            old = Image.objects.get(pk=self.id)
            if self.url != old.url:
                if old.pk:
                    old.url.delete(save=False)
        except Image.DoesNotExist:
            return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.glasses.name} - {self.description}"

    class Meta:
        verbose_name = _("Imagem")
        verbose_name_plural = _("Imagens")
        ordering = ["glasses"]
