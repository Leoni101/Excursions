import re
from datetime import date

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from users.models import User
from .models import Category, Excursion

ALLOWED_SORTS = {
    "title": "title",
    "-title": "-title",
    "price": "price",
    "-price": "-price",
    "duration": "duration",
    "-duration": "-duration",
    "popular": "-active_bookings_count",
}


def excursion_list(request):
    queryset = (
        Excursion.objects.select_related("category")
        .filter(is_active=True)
        .annotate(
            active_bookings_count=Count(
                "bookings", filter=Q(bookings__is_cancelled=False)
            )
        )
    )

    category_slug = request.GET.get("category", "").strip()
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    max_price = request.GET.get("max_price", "").strip()
    if max_price.isdigit():
        queryset = queryset.filter(price__lte=int(max_price))

    sort_param = request.GET.get("sort", "title")
    queryset = queryset.order_by(ALLOWED_SORTS.get(sort_param, "title"))

    search_query = request.GET.get("q", "").strip()
    if search_query:
        q_lower = search_query.lower()
        matching_ids = [
            exc.id
            for exc in queryset
            if q_lower in exc.title.lower() or q_lower in exc.description.lower()
        ]
        queryset = queryset.filter(id__in=matching_ids)

    filtered_summary = queryset.aggregate(
        found_count=Count("id"),
        avg_price=Avg("price"),
    )

    paginator = Paginator(queryset, 4)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "excursions": page_obj.object_list,
        "categories": Category.objects.all(),
        "search_query": search_query,
        "selected_category": category_slug,
        "max_price": max_price,
        "sort_param": sort_param,
        "filtered_summary": filtered_summary,
    }
    return render(request, "excursions/excursion_list.html", context)


def excursion_detail(request, excursion_id):
    excursion = get_object_or_404(
        Excursion.objects.select_related("category"),
        pk=excursion_id,
    )

    form_data = {
        "full_name": "",
        "email": "",
        "phone": "",
        "date": "",
        "participants": "1",
    }

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        booking_date_str = request.POST.get("date", "").strip()
        participants_str = request.POST.get("participants", "1").strip()

        form_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "date": booking_date_str,
            "participants": participants_str,
        }

        digits_only = re.sub(r"\D", "", phone)

        if not full_name or len(full_name) < 2 or any(ch.isdigit() for ch in full_name):
            messages.error(
                request,
                "Укажите корректное ФИО (без цифр, минимум 2 символа).",
            )
        elif not phone or not (10 <= len(digits_only) <= 15):
            messages.error(
                request,
                "Укажите корректный номер телефона (от 10 до 15 цифр).",
            )
        else:
            try:
                booking_date = date.fromisoformat(booking_date_str)
                participants = int(participants_str)

                already_booked = Booking.objects.filter(
                    excursion=excursion,
                    date=booking_date,
                    is_cancelled=False,
                ).exists()

                if already_booked:
                    messages.error(
                        request,
                        "На эту дату экскурсия уже забронирована. Выберите другой день.",
                    )
                else:
                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={"full_name": full_name, "phone": phone},
                    )
                    if not created:
                        user.full_name = full_name
                        user.phone = phone
                        user.save(update_fields=["full_name", "phone"])

                    booking = Booking(
                        excursion=excursion,
                        user=user,
                        date=booking_date,
                        participants=participants,
                    )
                    booking.full_clean()
                    booking.save()
                    messages.success(request, f"Бронирование №{booking.id} успешно создано!")
                    return redirect("bookings:booking_detail", booking_id=booking.id)
            except (ValueError, ValidationError) as exc:
                messages.error(request, f"Ошибка при бронировании: {exc}")

    upcoming_bookings = (
        excursion.bookings.select_related("user")
        .filter(is_cancelled=False)
        .exclude(date__lt=date.today())
        .order_by("date")
    )

    context = {
        "excursion": excursion,
        "upcoming_bookings": upcoming_bookings,
        "today_iso": date.today().isoformat(),
        "form_data": form_data,
    }
    return render(request, "excursions/excursion_detail.html", context)


def available_excursions(request):
    selected_date_str = request.GET.get("date", date.today().isoformat()).strip()
    try:
        target_date = date.fromisoformat(selected_date_str)
    except ValueError:
        target_date = date.today()
        selected_date_str = target_date.isoformat()

    free_excursions = (
        Excursion.objects.select_related("category")
        .filter(is_active=True)
        .exclude(bookings__date=target_date, bookings__is_cancelled=False)
        .order_by("price")
    )

    context = {
        "free_excursions": free_excursions,
        "selected_date": selected_date_str,
        "today_iso": date.today().isoformat(),
    }
    return render(request, "excursions/available.html", context)
