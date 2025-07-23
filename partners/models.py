from django.db import models

class Partner:
    name = models.TextField(
        'Название',
        help_text='Название организации партнера',
    )
    
    url = models.URLField(
        'Ссылка',
        blank=True,
        help_text='Ссылка на организацию партнера',
    )
    
    img = models.ImageField(
        'Картинка',
        upload_to='images/partners',
        help_text='Изображение логотипа партнёра',
    )
    
    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'