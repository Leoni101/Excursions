import json
import os
from models import Excursion, Booking


def load_excursions(filename):
    if not os.path.exists(filename):
        return []

    file = open(filename, "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    excursions = []
    for item in data:
        exc = Excursion(item["id"], item["title"],
                        item["price"], item["duration"])
        excursions.append(exc)
    return excursions


def save_excursions(filename, excursions):
    data = []
    for exc in excursions:
        data.append({
            "id": exc.id,
            "title": exc.title,
            "price": exc.price,
            "duration": exc.duration
        })

    file = open(filename, "w", encoding="utf-8")
    json.dump(data, file, ensure_ascii=False, indent=4)
    file.close()


def load_bookings(filename, excursions):
    if not os.path.exists(filename):
        return []

    file = open(filename, "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    bookings = []
    for item in data:
        # Ищем нужную экскурсию
        found_excursion = None
        for exc in excursions:
            if exc.id == item["excursion_id"]:
                found_excursion = exc
                break

        if found_excursion is not None:
            book = Booking(item["id"], found_excursion, item["date"])
            book.is_cancelled = item["is_cancelled"]
            bookings.append(book)

    return bookings


def save_bookings(filename, bookings):
    data = []
    for book in bookings:
        data.append({
            "id": book.id,
            "excursion_id": book.excursion.id,
            "date": book.date,
            "is_cancelled": book.is_cancelled
        })

    file = open(filename, "w", encoding="utf-8")
    json.dump(data, file, ensure_ascii=False, indent=4)
    file.close()
