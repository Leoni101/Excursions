def is_excursion_available(bookings: list[dict], excursion_id: int, booking_date: str) -> bool:
    for b in bookings:
        if b["excursion_id"] == excursion_id and b["date"] == booking_date:
            return False
    return True

def create_booking(bookings: list[dict], excursion_id: int, booking_date: str) -> dict | None:
    if not is_excursion_available(bookings, excursion_id, booking_date):
        return None
    
    new_id = max([b["id"] for b in bookings], default=0) + 1
    booking = {
        "id": new_id,
        "excursion_id": excursion_id,
        "date": booking_date
    }
    bookings.append(booking)
    return booking

def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    for i, b in enumerate(bookings):
        if b["id"] == booking_id:
            del bookings[i]
            return True
    return False