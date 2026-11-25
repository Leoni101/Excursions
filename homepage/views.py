from django.db.models import Avg, Count, Q
from django.shortcuts import render

from bookings.models import Booking
from excursions.models import Category, Excursion


def index(request):
    """Главная страница проекта со сводной статистикой из ORM."""
    stats = Excursion.objects.filter(is_active=True).aggregate(
        total=Count("id"),
        avg_price=Avg("price"),
    )
    active_bookings = Booking.objects.filter(is_cancelled=False).count()

    popular_excursions = (
        Excursion.objects.select_related("category")
        .filter(is_active=True)
        .annotate(
            active_bookings_count=Count(
                "bookings", filter=Q(bookings__is_cancelled=False)
            )
        )
        .order_by("-active_bookings_count", "price")[:3]
    )

    categories = Category.objects.annotate(
        excursions_count=Count("excursions", filter=Q(excursions__is_active=True))
    )

    return render(
        request,
        "homepage/index.html",
        {
            "stats": stats,
            "active_bookings": active_bookings,
            "popular_excursions": popular_excursions,
            "categories": categories,
        },
    )
