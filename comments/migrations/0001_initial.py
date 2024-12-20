# Generated by Django 5.0.6 on 2024-12-13 08:16

import comments.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('text', models.TextField(max_length=1000)),
                ('title', models.CharField(max_length=120, verbose_name='Titulo')),
                ('rating', models.IntegerField(choices=[(1, '1 Estrela'), (2, '2 Estrelas'), (3, '3 Estrelas'), (4, '4 Estrelas'), (5, '5 Estrelas')], verbose_name='Avaliação')),
                ('has_images', models.BooleanField(default=False, verbose_name='Há imagens?')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='color_comment', to='data.color')),
                ('glasses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_glasses', to='data.glasses', verbose_name='Oculos')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_user', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CommentsMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=comments.models.CommentsMedia.create_image_path, verbose_name='Imagem')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_comments', to='comments.comments', verbose_name='Comentario')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
