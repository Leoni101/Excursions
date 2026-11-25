from django.db import models


class User(models.Model):

    full_name = models.CharField("ФИО / Имя", max_length=120)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=30, blank=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"
