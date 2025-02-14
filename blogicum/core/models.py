from django.db import models


class PublishedModel(models.Model):
    """Абстрактная модель. Добвляет флаг is_published."""

    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    """Абстрактная модель, добавляет поле 'created_at'."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    """Абстрактная модель, добавляет поле 'title'."""

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Заголовок',
    )

    class Meta:
        abstract = True
