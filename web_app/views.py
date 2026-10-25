from django.shortcuts import render
from db.database import get_connection


def index(request):
    return render(request, "web_app/index.html")


def excursion_list(request):
    conn = get_connection()
    excursions = conn.execute(
        "SELECT id, title, price FROM excursions ORDER BY title").fetchall()
    conn.close()

    context = {"excursions": excursions}
    return render(request, "web_app/excursion_list.html", context)


def excursion_detail(request, excursion_id):
    conn = get_connection()
    excursion = conn.execute(
        "SELECT id, title, price, duration FROM excursions WHERE id = ?",
        (excursion_id,)
    ).fetchone()
    conn.close()

    context = {"excursion": excursion}
    status_code = 404 if excursion is None else 200

    return render(request, "web_app/excursion_detail.html", context, status=status_code)


def booking_list(request):
    conn = get_connection()
    bookings = conn.execute("""
        SELECT bookings.id, bookings.date, bookings.is_cancelled, excursions.title 
        FROM bookings 
        JOIN excursions ON bookings.excursion_id = excursions.id
        ORDER BY bookings.date
    """).fetchall()
    conn.close()

    context = {"bookings": bookings}
    return render(request, "web_app/booking_list.html", context)
