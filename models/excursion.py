class Excursion:
    def __init__(self, excursion_id, title, price, duration):
        self.id = excursion_id
        self.title = title
        self.price = price
        self.duration = duration

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.price} руб."