from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, SET_NULL

from core.models import PublishedModel
from .constants import CATEGORY_STR_LENGTH, POST_STR_LENGTH, TITLE_MAX_LENGTH


User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Category(PublishedModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:CATEGORY_STR_LENGTH]


class Location(PublishedModel):
    name = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно '
        'делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta(PublishedModel.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:POST_STR_LENGTH]
