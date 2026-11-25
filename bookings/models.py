from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from excursions.models import Excursion
from users.models import User


class Booking(models.Model):
    """Модель бронирования со связями ForeignKey на Excursion и User (5.5.3)."""

    excursion = models.ForeignKey(
        Excursion,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Экскурсия",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    date = models.DateField("Дата экскурсии")
    participants = models.PositiveIntegerField(
        "Количество участников",
        default=1,
        validators=[MinValueValidator(1)],
    )
    is_cancelled = models.BooleanField("Отменено", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-date", "-id"]
        indexes = [
            models.Index(fields=["date", "is_cancelled"]),
        ]

    def clean(self) -> None:
        if self.excursion_id and not self.excursion.is_active:
            raise ValidationError("Нельзя забронировать неактивную экскурсию.")
        if self.date and self.date < timezone.localdate() and not self.pk:
            raise ValidationError("Дата бронирования не может быть в прошлом.")

    def __str__(self) -> str:
        return f"Бронь №{self.id}: {self.excursion.title} ({self.user.full_name}, {self.date})"
