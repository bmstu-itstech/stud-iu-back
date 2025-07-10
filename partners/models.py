from django.db import models

class Partner:
    name = models.CharField(
        'Название',
        max_length=50,
        help_text='Название организации партнера',
    )
    
    url = models.URLField(
        'Ссылка',
        blank=True,
        help_text='Ссылка на организацию партнера',
    )
    
    img = models.ImageField(
        'Картинка',
        upload_to='partners',
        help_text='Изображение логотипа партнёра',
    )
    
    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'