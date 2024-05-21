from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(is_published=ArticleModel.Status.PUBLISHED)


class ArticleModel(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(
        max_length=255,
        verbose_name='Название статьи',
    )

    slug = AutoSlugField(populate_from='name')

    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Краткое описание',
    )

    content = models.TextField(
        verbose_name='Текст статьи',
    )

    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED,
        verbose_name="Статус",
    )

    time_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создание статьи',
    )

    time_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Время изменения',
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='posts',
        null=True,
        default=None,
        verbose_name='Автор статьи'
    )

    cat = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория',
    )

    photo = models.ImageField(
        upload_to='photo/articles/%Y/%m/%d',
        blank=True,
        default=None,
        null=True,
        verbose_name='Фото'
    )

    published = PublishedManager()

    objects = models.Manager()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("show_post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'

        ordering = [
            '-time_created',
        ]

        indexes = [
            models.Index(fields=['-time_created'])
        ]


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Имя категории',
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        verbose_name='cat_slug'
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})


class Comments(models.Model):
    article = models.ForeignKey(
        'ArticleModel',
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        validators=[
            MinLengthValidator(5, 'Минимальная длинна комментария 5 символов')
        ],
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Комментарий от {self.author} к посту {self.article}'
