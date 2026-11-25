from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from excursions.models import Excursion
from users.models import User
from .models import Booking


def booking_list(request):
    """Список бронирований с select_related, фильтрацией и пагинацией."""
    bookings_qs = Booking.objects.select_related(
        "excursion", "excursion__category", "user"
    ).all()

    status_filter = request.GET.get("status", "all")
    if status_filter == "active":
        bookings_qs = bookings_qs.filter(is_cancelled=False)
    elif status_filter == "cancelled":
        bookings_qs = bookings_qs.filter(is_cancelled=True)

    q = request.GET.get("q", "").strip()
    if q:
        q_lower = q.lower()
        matching_ids = [
            b.id
            for b in bookings_qs
            if q_lower in b.excursion.title.lower() or q_lower in b.user.full_name.lower()
        ]
        bookings_qs = bookings_qs.filter(id__in=matching_ids)

    paginator = Paginator(bookings_qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "bookings": page_obj.object_list,
        "status_filter": status_filter,
        "q": q,
    }
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    """Карточка бронирования (аналог booking_detail.html из методички)."""
    booking = get_object_or_404(
        Booking.objects.select_related("excursion", "excursion__category", "user"),
        pk=booking_id,
    )
    total_cost = booking.excursion.price * booking.participants
    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking, "total_cost": total_cost},
    )


@require_POST
def cancel_booking(request, booking_id):
    """Отмена бронирования через ORM."""
    booking = get_object_or_404(Booking, pk=booking_id)
    if not booking.is_cancelled:
        booking.is_cancelled = True
        booking.save(update_fields=["is_cancelled"])
        messages.info(request, f"Бронирование №{booking.id} отменено.")
    return redirect("bookings:booking_list")


def statistics(request):
    """Страница ORM-статистики (аналог statistics.html из пункта 5.12 методички)."""
    booking_summary = Booking.objects.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(is_cancelled=False)),
        cancelled=Count("id", filter=Q(is_cancelled=True)),
        total_participants=Sum("participants", filter=Q(is_cancelled=False)),
    )

    excursion_summary = Excursion.objects.filter(is_active=True).aggregate(
        total=Count("id"),
        avg_price=Avg("price"),
        min_price=Min("price"),
        max_price=Max("price"),
    )

    # Аннотирование экскурсий: количество активных броней и сумма участников
    by_excursion = (
        Excursion.objects.annotate(
            bookings_count=Count("bookings", filter=Q(bookings__is_cancelled=False)),
            guests_sum=Sum("bookings__participants", filter=Q(bookings__is_cancelled=False)),
        )
        .order_by("-bookings_count", "title")
    )

    # Аннотирование пользователей по числу броней
    top_users = (
        User.objects.annotate(
            bookings_count=Count("bookings", filter=Q(bookings__is_cancelled=False))
        )
        .filter(bookings_count__gt=0)
        .order_by("-bookings_count")
    )

    context = {
        "booking_summary": booking_summary,
        "excursion_summary": excursion_summary,
        "by_excursion": by_excursion,
        "top_users": top_users,
    }
    return render(request, "bookings/statistics.html", context)
