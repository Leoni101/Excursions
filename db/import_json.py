import json
from db.database import get_connection


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def main():
    conn = get_connection()

    conn.execute("DELETE FROM bookings")
    conn.execute("DELETE FROM excursions")

    excursions = load_json("data/excursions.json")
    for e in excursions:
        conn.execute(
            "INSERT INTO excursions (id, title, price, duration) VALUES (?, ?, ?, ?)",
            (e["id"], e["title"], e["price"], e["duration"])
        )

    bookings = load_json("data/bookings.json")
    for b in bookings:
        conn.execute(
            "INSERT INTO bookings (id, excursion_id, date, is_cancelled) VALUES (?, ?, ?, ?)",
            (b["id"], b["excursion_id"], b["date"], int(b["is_cancelled"]))
        )

    conn.commit()
    conn.close()
    print("Данные успешно импортированы в SQLite!")


if __name__ == "__main__":
    main()
