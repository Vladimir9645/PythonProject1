

"""Обрабатывает информацию как о картах, так и о счетах."""



from src.masks import get_mask_account, get_mask_card_number


#Функция
def mask_account_card():
    """Обрабатывает информацию как о картах, так и о счетах."""
    card_types = ['Maestro', 'MasterCard', 'Visa Classic', 'Visa Platinum', 'Visa Gold'] # Список карт
    account_types = ['Счет'] # Список счет

    account_card = input("Введите название карты или счета: ").strip() # - Убирает лишние пробелы вокруг текста.
    # Помогает избежать ошибок при вводе данных, если пользователь случайно добавил пробелы.
    if account_card in card_types: # Проверяем есть-ли в списке вводамая карта.
        number = input("Введите номер карты (16 цифр): ").strip() # Ввод номера карты
        return f"{account_card} {get_mask_card_number(number)}"  # Нашу функцию ставим 1 затем функц маски. При вызове.
    elif account_card in account_types: # Проверяем список если указали Счет.
        number = input("Введите номер счёта (20 цифр): ").strip() # Тоже что и скартой только 20 цифр.
        return f"{account_card} {get_mask_account(number)}"  # Все тоже что и выше
    else:
        return "Неизвестный тип карты или счёта" # Если указаны не верные имена Карт и Счет.
# Пример вызова
print(mask_account_card()) # Вызов функции.



""" Принимает строку с датой в формате "2024-03-11T02:26:18.671407" 
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" """



from datetime import datetime


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формает и возвращает строку с датой."""
    # Переносим входную строку в объект datetime
    dt = datetime.fromisoformat(date_str)
    # Форматируем дату в нужный формат: День.Месяц.Год
    return dt.strftime("%d.%m.%Y")

# Пример использования:
print(get_date("2024-03-11T02:26:18.671407"))  # Выведет: 11.03.2024
