from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):

    name = models.CharField("Название категории", max_length=100, unique=True)
    slug = models.SlugField("URL-код", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Excursion(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="excursions",
        verbose_name="Категория",
    )
    title = models.CharField("Название экскурсии", max_length=200)
    description = models.TextField("Описание программы", blank=True)
    price = models.DecimalField(
        "Цена (руб.)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    duration = models.PositiveIntegerField(
        "Длительность (ч.)",
        validators=[MinValueValidator(1)],
    )
    is_active = models.BooleanField("Доступна", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Экскурсия"
        verbose_name_plural = "Экскурсии"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.price} руб.)"
