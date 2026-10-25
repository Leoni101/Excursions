from django.shortcuts import render
from storage import load_excursions, load_bookings

def index(request):
    return render(request, "web_app/index.html")

def excursion_list(request):
    excursions = load_excursions("data/excursions.json")
    context = {"excursions": excursions}
    return render(request, "web_app/excursion_list.html", context)

def excursion_detail(request, excursion_id):
    excursions = load_excursions("data/excursions.json")
    
    excursion = None
    for e in excursions:
        if e.id == excursion_id:
            excursion = e
            break

    context = {"excursion": excursion}
    
    status_code = 404 if excursion is None else 200
    return render(request, "web_app/excursion_detail.html", context, status=status_code)

def booking_list(request):
    excursions = load_excursions("data/excursions.json")
    bookings = load_bookings("data/bookings.json", excursions)
    context = {"bookings": bookings}
    return render(request, "web_app/booking_list.html", context)