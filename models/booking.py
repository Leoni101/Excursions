class Booking:
    def __init__(self, booking_id, excursion, date):
        self.id = booking_id
        self.excursion = excursion
        self.date = date
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True

    def __str__(self):
        status = "Отменено" if self.is_cancelled else "Активно"
        return f"[{self.id}] {self.excursion.title} на {self.date} ({status})"