import json
import os
import sqlite3
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "excursion_web.settings")

import django

django.setup()

from bookings.models import Booking
from excursions.models import Category, Excursion
from users.models import User


def run_import():
    cat_city, _ = Category.objects.get_or_create(
        slug="city-tours",
        defaults={"name": "Городские прогулки", "description": "Обзорные экскурсии по городу"},
    )
    cat_museum, _ = Category.objects.get_or_create(
        slug="museums",
        defaults={"name": "Музеи и галереи", "description": "Посещение главных музеев"},
    )
    cat_outskirt, _ = Category.objects.get_or_create(
        slug="outskirts",
        defaults={"name": "Загородные маршруты", "description": "Усадьбы и исторические города"},
    )

    # 1. Импорт из data/excursions.json
    json_path = BASE_DIR / "data" / "excursions.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                cat = cat_museum if "галере" in item["title"].lower() else cat_city
                Excursion.objects.update_or_create(
                    id=item["id"],
                    defaults={
                        "title": item["title"],
                        "price": Decimal(str(item["price"])),
                        "duration": item["duration"],
                        "category": cat,
                        "description": f"Подробная программа маршрута «{item['title']}».",
                    },
                )

    extra = [
        ("Огни ночной Москвы", cat_city, Decimal("1800.00"), 2, "Вечерний маршрут по набережным."),
        ("Тайны Московского Кремля", cat_museum, Decimal("2500.00"), 4, "Экскурсия по территории Кремля."),
        ("Усадьба Архангельское", cat_outskirt, Decimal("2200.00"), 5, "Прогулка по дворцовому парку."),
        ("Сергиев Посад и Лавра", cat_outskirt, Decimal("3100.00"), 7, "Путешествие по Золотому кольцу."),
        ("Архитектура старого Арбата", cat_city, Decimal("1200.00"), 2, "Пешеходная прогулка по переулкам."),
    ]
    for title, cat, price, duration, desc in extra:
        Excursion.objects.get_or_create(
            title=title,
            defaults={"category": cat, "price": price, "duration": duration, "description": desc},
        )

    # 2. Создание пользователей
    u1, _ = User.objects.get_or_create(
        email="anna@example.com",
        defaults={"full_name": "Анна Смирнова", "phone": "+7 (999) 111-22-33"},
    )
    u2, _ = User.objects.get_or_create(
        email="ivan@example.com",
        defaults={"full_name": "Иван Петров", "phone": "+7 (999) 444-55-66"},
    )

    # 3. Перенос броней из data/excursion.sqlite (если есть)
    legacy_db = BASE_DIR / "data" / "excursion.sqlite"
    if legacy_db.exists():
        conn = sqlite3.connect(legacy_db)
        conn.row_factory = sqlite3.Row
        try:
            for row in conn.execute("SELECT id, excursion_id, date, is_cancelled FROM bookings"):
                exc = Excursion.objects.filter(id=row["excursion_id"]).first()
                if exc:
                    Booking.objects.update_or_create(
                        id=row["id"],
                        defaults={
                            "excursion": exc,
                            "user": u1,
                            "date": row["date"],
                            "is_cancelled": bool(row["is_cancelled"]),
                        },
                    )
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()

    if Booking.objects.count() == 0:
        all_exc = list(Excursion.objects.all()[:2])
        if len(all_exc) >= 2:
            Booking.objects.create(excursion=all_exc[0], user=u1, date=date.today() + timedelta(days=3), participants=2)
            Booking.objects.create(excursion=all_exc[1], user=u2, date=date.today() + timedelta(days=5), participants=1)
            Booking.objects.create(excursion=all_exc[0], user=u2, date=date.today() + timedelta(days=1), participants=3, is_cancelled=True)

    print(f"Импорт завершён: экскурсий={Excursion.objects.count()}, пользователей={User.objects.count()}, броней={Booking.objects.count()}")


if __name__ == "__main__":
    run_import()