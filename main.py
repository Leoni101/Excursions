from datetime import date

excursion_title = "Обзорная экскурсия по городу"
excursion_price = 1500.0          # float
excursion_duration = 3            # int (часы)
excursion_available = True        # bool

booking_date = date(2026, 9, 15)
user_name = "Лиза"
user_age = 20


# Функция 1: информация об экскурсии
def get_excursion_info(title, price, duration): #Возвращает строку с информацией об экскурсии.
    info = (
        f"Экскурсия: {title}\n"
        f"Стоимость: {price} руб.\n"
        f"Длительность: {duration} ч."
    )
    return info


# Функция 2: проверка доступности даты
def is_date_available(is_available, booking_day): #Проверяет, доступна ли дата для бронирования.
    if is_available:
        return f"Дата {booking_day} доступна для бронирования"
    else:
        return f"Дата {booking_day} недоступна"


# Функция 3: расчёт стоимости
def calculate_total_price(price, persons): #Считает итоговую стоимость для нескольких человек.
    if persons <= 0:
        return "Количество человек должно быть больше нуля"
    total = price * persons
    return f"Итоговая стоимость для {persons} чел.: {total} руб."


print("Сервис бронированя экскурсий \n")

# 1. Показываем информацию об экскурсии
print(get_excursion_info(excursion_title, excursion_price, excursion_duration))

# 2. Проверяем доступность даты
print(is_date_available(excursion_available, booking_date))

# 3. Считаем стоимость для 2 человек
persons = int(input("Сколько человек хотите записать? "))
print(calculate_total_price(excursion_price, persons))
