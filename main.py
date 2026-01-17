import os
from typing import Callable
from datetime import datetime

# Ваши импорты
from src.financial_transactions_CSV import read_transactions_from_csv
from src.financial_transactions_Excel import read_transactions_from_excel
from src.generators import filter_by_currency, count_operations_by_category
from src.processing import filter_by_state, sort_by_date
from src.utils import dictionary_with_transaction_data
from src.widget import mask_account_card

print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
status = ["EXECUTED", "CANCELED", "PENDING"]


def main():
    dict_file = {
        1: dictionary_with_transaction_data,
        2: read_transactions_from_csv,
        3: read_transactions_from_excel
    }
    path_file = {
        1: os.path.join(DATA_DIR, "operations.json"),
        2: os.path.join(DATA_DIR, "transactions.csv"),
        3: os.path.join(DATA_DIR, "transactions_excel.xlsx")
    }

    # Шаг 1. Выбор источника данных
    while True:
        print(
            "Выберите необходимый пункт меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла"
        )
        try:
            user_input: int = int(input("Пользователь: "))
        except ValueError:
            print("Ошибка: введите число от 1 до 3.")
            continue

        get_func: Callable | None = dict_file.get(user_input)
        if not get_func:
            print("Неверный выбор.")
            continue

        path_: str | None = path_file.get(user_input)
        if path_ is None:
            print("Путь к файлу не найден.")
            continue

        transaction = get_func(path_)
        break

    # Флаг: применялась ли хоть одна фильтрация/сортировка
    filtered = False

    # Шаг 2. Фильтрация по статусу
    print("Введите статус, по которому необходимо выполнить фильтрацию.\n"
          f"Доступные для фильтровки статусы: {', '.join(status)}")
    user_input_status: str = input("Пользователь: ").upper()
    if user_input_status in status:
        transaction = filter_by_state(transaction, user_input_status)
        print(f"Операции отфильтрованы по статусу {user_input_status}")
        filtered = True
    else:
        print(f"Статус операции '{user_input_status}' недоступен.")

    # Шаг 3. Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    if input("Пользователь: ").lower() == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        user_sort_reverse: bool = input("Пользователь: ").lower() == "по убыванию"
        transaction = sort_by_date(transaction, reverse=user_sort_reverse)
        filtered = True

    # Шаг 4. Фильтрация по валюте
    print("Выводить только рублевые транзакции? Да/Нет")
    if input("Пользователь: ").lower() == "да":
        transaction = list(filter_by_currency(transaction, "RUB"))
        filtered = True

    # Шаг 5. Поиск по слову в описании
    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    if input("Пользователь: ").lower() == "да":
        print("Введите слово для фильтрации:")
        try:
            search_word: str = input("Пользователь: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("Ввод прерван.")
            return

        categories = [
            "Открытие вклада",
            "Перевод с карты на карту",
            "Перевод организации",
            "Перевод со счета на счет"
        ]

        counts = count_operations_by_category(transaction, search_word, categories)
        total_found = sum(counts.values())

        if total_found == 0:
            print("Транзакции не найдены, попробуйте другой статус")
        else:
            print(f"Найдено транзакций: {total_found}")
            print("Количество операций по категориям:")
            for category, count in counts.items():
                print(f"{category}: {count}")

        filtered = True

    # Шаг 6. Финальный вывод результатов
    if not filtered:
        print("\nНи одна фильтрация не была применена. Выводится исходный список транзакций:")
    else:
        print("\nВыводится обработанный список транзакций:")

    if transaction:
        for trans in transaction:
            state = trans.get("state")
            date_str = trans.get("date")
            try:
                if date_str:
                    date_formats = [
                        "%Y-%m-%dT%H:%M:%S.%fZ",  # 2023-01-01T12:34:56.789Z
                        "%Y-%m-%dT%H:%M:%SZ",  # 2023-01-01T12:34:56Z
                        "%Y-%m-%d %H:%M:%S",  # 2023-01-01 12:34:56
                        "%d.%m.%Y %H:%M:%S",  # 01.01.2023 12:34:56
                        "%Y-%m-%d"  # 2023-01-01
                    ]
                    date = "Некорректная дата"
                    for fmt in date_formats:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt)
                            date = parsed_date.strftime("%d.%m.%Y")
                            break  # Успех — выходим из цикла
                        except ValueError:
                            continue  # Пробуем следующий формат
                else:
                    date = "Неизвестно"
            except ValueError:
                date = "Некорректная дата"

            amount = trans.get("amount")
            currency_name = trans.get("currency_name")
            to_from = trans.get("from")
            to = mask_account_card(trans.get("to"))
            description = trans.get("description")

            out_print = f"{date} {description}"
            check_to = f"{to}"
            check_from = " -> " + mask_account_card(to_from) if to_from and isinstance(to_from, str) else ""
            summ_print = f" сумма {amount} {currency_name}."

            print(f"{out_print}\n{check_to}{check_from}\n{summ_print}\n")
    else:
        print("Транзакции отсутствуют.")

if __name__ == "__main__":
    main()

