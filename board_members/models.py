from django.db import models


class BoardMember(models.Model):
    name = models.TextField(
        'ФИО',
        help_text="Фамилия, имя и отчество члена руководящего состава, например, Николай Эрнестович Бауман"
    )
    telegram_link = models.TextField(
        'Телеграм',
        help_text='Ссылка на профиль в Telegram'
    )
    position = models.TextField(
        'Должность',
    )
    start_date = models.DateField(
        'Дата вступления в должность',
        help_text='Дата вступления в должность, например, 11.05.2006',
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        'Изображение',
        upload_to="images/board_member/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}: {self.position}"

    class Meta:
        verbose_name = 'Член руководящего состава'
        verbose_name_plural = 'Члены руководящего состава'
