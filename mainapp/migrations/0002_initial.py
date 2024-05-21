# Generated by Django 4.2.1 on 2024-04-05 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор статьи'),
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='mainapp.category', verbose_name='Категория'),
        ),
        migrations.AddIndex(
            model_name='articlemodel',
            index=models.Index(fields=['-time_created'], name='mainapp_art_time_cr_361b68_idx'),
        ),
    ]
