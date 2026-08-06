import uuid

from django.db import models


class BoardMember(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        "ФИО",
        help_text="Фамилия, имя и отчество члена руководящего состава, например, Николай Эрнестович Бауман",
        max_length=256,
    )
    link = models.URLField(
        "Ссылка",
    )
    position = models.CharField(
        "Должность",
        max_length=256,
    )
    image = models.ImageField(
        "Изображение",
        upload_to="images/board_member/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Член руководящего состава"
        verbose_name_plural = "Члены руководящего состава"

    def __str__(self):
        return f"{self.name}: {self.position}"
