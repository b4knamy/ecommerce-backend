from django.db.models.signals import post_save
from django.dispatch import receiver
from data.models import Glasses, Model,  Color
from django.utils.text import slugify


# @receiver(post_save, sender=Glasses)
# def create_glasses_slug(sender, instance, created, **kwargs):
#     if created and not instance.slug:

#         instance.slug = slugify(instance.name)
#         instance.save()


# @receiver(post_save, sender=Model)
# def create_model_slug(sender, instance, created, **kwargs):
#     if created and not instance.slug:
#         instance.slug = slugify(instance.modelo)
#         instance.save()


# @receiver(post_save, sender=Color)
# def create_color_slug(sender, instance, created, **kwargs):
#     if created and not instance.slug:
#         instance.slug = slugify(instance.name)
#         instance.save()


# @receiver(post_save, sender=OculosType)
# def create_oculos_type_slug(sender, instance, created, **kwargs):
#     if created and not instance.slug:
#         instance.slug = slugify(instance.oculos_type)
#         instance.save()
