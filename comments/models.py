from django.db import models
from data.models import Glasses, Color
from authentication.models import User
from django.utils.translation import gettext_lazy as _
from data.models import AbstractTimeStamp


class Comments(AbstractTimeStamp):
    edited_at = None

    glasses = models.ForeignKey(Glasses, verbose_name=_(
        "Oculos"), related_name="comments_glasses", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_(
        "Usuário"), related_name="comments_user", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    color = models.ForeignKey(
        Color, models.SET_NULL, related_name="color_comment", null=True, blank=True)
    title = models.CharField(_("Titulo"), max_length=120)
    rating = models.IntegerField(_("Avaliação"), choices={
        1: "1 Estrela",
        2: "2 Estrelas",
        3: "3 Estrelas",
        4: "4 Estrelas",
        5: "5 Estrelas",
    })
    has_images = models.BooleanField(_("Há imagens?"), default=False)

    def __str__(self):
        return f'"{self.title}" - do Oculos "{self.glasses.name}" feito por "{self.user.get_full_name()}"'

    def delete(self, *args, **kwargs):

        for image in self.images.all():
            image.delete()

        return super().delete(*args, **kwargs)

    class Meta:
        ordering = ["id"]


class CommentsMedia(models.Model):

    def create_image_path(self, file):

        return f"""comments/{self.comment.glasses.slug}/{self.comment.user.get_full_name().replace(" ", "-").lower()}/{file}"""

    comment = models.ForeignKey(Comments, verbose_name=_(
        "Comentario"), related_name="images_comments", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Imagem',
                              upload_to=create_image_path, max_length=100)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)

        return super().delete(*args, **kwargs)

    class Meta:
        ordering = ["id"]
