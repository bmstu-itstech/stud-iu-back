from django.db import models
from django.utils import timezone

class News(models.Model):
    title = models.CharField(
        'Название',
        max_length=128,
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )
    cover = models.ImageField(
        'Обложка',
        upload_to='images/news/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        'Дата',
        default=timezone.now,
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
