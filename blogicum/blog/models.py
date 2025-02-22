from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import Count

from core.models import PublishedModel, CreatedAtModel, TitleModel

User = get_user_model()


class PostManager(models.Manager):
    # Посты для простых посетителей.
    def posts_objects(self):
        return self.get_queryset().select_related(
            'category',
            'author',
            'location',
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now(),
        )
    # Посты для владельцев постов.

    def posts_with_annotate(self):
        return self.get_queryset().order_by(
            '-pub_date').annotate(comment_count=Count('comment_post'))

    # Посты для владельцев постов со счетчиком комментариев.
    def posts_with_annotate(self):
        return self.get_queryset().order_by(
            '-pub_date').annotate(comment_count=Count('comment_post'))

    # Посты для простых посетителей со счетчиком комментариев.
    def posts_object_with_annotate(self):
        return self.get_queryset().select_related(
            'category',
            'author',
            'location',
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now(),
        ).order_by(
            '-pub_date').annotate(comment_count=Count('comment_post'))


class CategoryManager(models.Manager):
    # Категория для простых посетителей
    def category(self):
        return self.get_queryset().filter(
            is_published=True,
            created_at__lte=now(),
        )

    # Категория для простых посетителей со счетчиком комментариев.
    def category_with_annotate(self):
        return self.get_queryset().filter(
            is_published=True,
            created_at__lte=now(),
        ).annotate(comment_count=Count('comment_category'))


class Post(PublishedModel, CreatedAtModel, TitleModel):
    text = models.TextField(
        blank=False,
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        blank=False,
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время '
        'в будущем — можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='Автор публикации',
        related_name='post_author',
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='location',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория',
        related_name='category',
    )
    image = models.ImageField('Фото', upload_to='posts_image', blank=True)
    objects = models.Manager()
    objects_manager = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Category(PublishedModel, CreatedAtModel, TitleModel):
    description = models.TextField(
        blank=False,
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    objects = models.Manager()
    objects_manager = CategoryManager()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel, CreatedAtModel):
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField('Комментарий', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='comment_category',
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        related_name='comment_post',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='comment_author',
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментаарии'

    def __str__(self):
        return self.text
