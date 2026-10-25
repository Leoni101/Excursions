def add_excursion(excursions: list[dict], title: str, price: float, duration: int) -> None:
    new_id = max([e["id"] for e in excursions], default=0) + 1
    excursions.append({
        "id": new_id,
        "title": title,
        "price": price,
        "duration": duration
    })

def find_excursion_by_id(excursions: list[dict], excursion_id: int) -> dict | None:
    for excursion in excursions:
        if excursion["id"] == excursion_id:
            return excursion
    return None

def show_excursions(excursions: list[dict]) -> None:
    for e in excursions:
        print(f"[{e['id']}] {e['title']} | Цена: {e['price']} руб. | Длительность: {e['duration']} ч.")