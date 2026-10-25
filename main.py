from storage import load_excursions, save_excursions, load_bookings, save_bookings
from models import Booking
from utils import input_int, input_date

EXCURSIONS_FILE = "data/excursions.json"
BOOKINGS_FILE = "data/bookings.json"

def main():
    excursions = load_excursions(EXCURSIONS_FILE)
    bookings = load_bookings(BOOKINGS_FILE, excursions)

    while True:
        print("\n=== МЕНЮ ===")
        print("1. Показать экскурсии")
        print("2. Забронировать")
        print("3. Отменить бронь")
        print("0. Выход")
        
        choice = input("Выберите пункт: ")
        
        if choice == "1":
            for e in excursions:
                print(e)
                
        elif choice == "2":
            for e in excursions:
                print(e)
            exc_id = input_int("Введите ID экскурсии: ")
            
            # Простой поиск экскурсии
            excursion = None
            for e in excursions:
                if e.id == exc_id:
                    excursion = e
                    break
            
            if excursion is None:
                print("Экскурсия не найдена.")
                continue
                
            date = input_date("Введите дату (ГГГГ-ММ-ДД): ")
            
            # Простая проверка на занятость
            busy = False
            for b in bookings:
                if b.excursion.id == exc_id and b.date == date and b.is_cancelled == False:
                    busy = True
                    break
                    
            if busy == True:
                print("Эта дата уже занята!")
            else:
                new_id = 1
                for b in bookings:
                    if b.id >= new_id:
                        new_id = b.id + 1
                        
                new_booking = Booking(new_id, excursion, date)
                bookings.append(new_booking)
                print("Успешно забронировано!")
                
        elif choice == "3":
            b_id = input_int("Введите ID брони: ")
            booking = None
            for b in bookings:
                if b.id == b_id:
                    booking = b
                    break
                    
            if booking is not None:
                booking.cancel()
                print("Бронь отменена.")
            else:
                print("Бронь не найдена.")
                
        elif choice == "0":
            break

    save_excursions(EXCURSIONS_FILE, excursions)
    save_bookings(BOOKINGS_FILE, bookings)
    print("Данные сохранены. Пока!")

if __name__ == "__main__":
    main()
