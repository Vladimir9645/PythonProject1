import os
from typing import Callable

from src.financial_transactions_CSV import read_transactions_from_csv
from src.financial_transactions_Excel import read_transactions_from_excel
from src.generators import filter_by_currency, count_operations_by_category
from src.processing import filter_by_state, sort_by_date
from src.utils import dictionary_with_transaction_data
from src.widget import mask_account_card
from datetime import datetime

print("""
Программа: Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
""")
BASE_DIR = os.path.dirname(__file__)
status = ["EXECUTED", "CANCELED", "PENDING"]

words_users: list[str] = [
    "Открытие вклада", "Перевод с карты на карту",
    "Перевод организации", "Перевод со счета на счет"
]

def main():
    dict_file = {
        1: dictionary_with_transaction_data,
        2: read_transactions_from_csv,
        3: read_transactions_from_excel
    }
    path_file = {1: BASE_DIR + "/data/operations.json",
                 2: BASE_DIR + "/data/transactions.csv",
                 3: BASE_DIR + "/data/transactions_excel.xlsx"}

    while True:
        print(
            "Выберите необходимый пункт меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла"
        )

        #user_input_status = input()
        user_input: int = int(input("Пользователь: "))
        get_func: Callable | None = dict_file.get(user_input)
        if get_func:
            print(get_func.__doc__)
            path_: str = path_file.get(user_input)
            transaction = get_func(path_)
            break

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.\n"
              f"Доступные для фильтровки статусы: {', '.join(status)}")
        user_input_status: str = input("Пользователь: ").upper()
        if user_input_status in status:
            transaction = filter_by_state(transaction, user_input_status)
            print(f"Операции отфильтрованы по статусу {user_input_status}")
            break
        else:
            print(f"Статус операции '{user_input_status}' недоступен.")
    print("Отсортировать операции по дате? Да/Нет")
    user_input: bool = input("Пользователь: ").lower() == "да"
    if user_input:
        print("Отсортировать по возрастанию или по убыванию?")
        user_sort_reverse: bool = input("Пользователь: ").lower() == "по убыванию"
        transaction = sort_by_date(transaction, reverse=user_sort_reverse)
    print("Выводить только рублевые транзакции? Да/Нет")
    user_input: bool = input("Пользователь: ").lower() == "да"
    if user_input:
        transaction = list(filter_by_currency(transaction, "RUB"))
    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    user_input: bool = input("Пользователь: ").lower() == "да"
    if user_input:
        print("Введите слово для фильтрации:")
        search_word: str = input("Пользователь: ").strip().lower()

        # Фильтруем транзакции: ищем слово в поле 'description'
        search_word_lower = search_word.lower()

        transaction_categories = [
            trans for trans in transaction
            if (
                    search_word_lower in str(trans.get("description", "")).strip() or
                    search_word_lower in str(trans.get("from", "")).strip() or
                    search_word_lower in str(trans.get("to", "")).strip()
            )
        ]

        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {(count_operations_by_category(transaction_categories, words_users))}")

        if not transaction_categories:
            print("По вашему запросу транзакции не найдены.")
            return

    for trans in transaction:
        state = trans.get("state")
        date_str = trans.get("date")
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        else:
            date = "Неизвестно"
        amount = trans.get("amount")
        currency_name = trans.get("currency_name")
        currency_code = trans.get("currency_code")
        to_from = trans.get("from")
        to = mask_account_card(trans.get("to"))
        description = trans.get("description")
        out_print = f"{date} {description}"
        check_to = f"{to}"
        check_from = " -> " + mask_account_card(to_from) if to_from else ""
        summ_print = f" сумма {amount}{currency_name}."
        print(f"{out_print}\n{check_to}{check_from}\n{summ_print}")
        """
            08.12.2019 Открытие вклада 
            Счет **4321
            Сумма: 40542 руб. 
            
            12.11.2019 Перевод с карты на карту
            MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203
            Сумма: 130 USD
            
            18.07.2018 Перевод организации 
            Visa Platinum 7492 65** **** 7202 -> Счет **0034
            Сумма: 8390 руб.
            
            03.06.2018 Перевод со счета на счет
            Счет **2935 -> Счет **4321
            Сумма: 8200 EUR
            """


if __name__ == "__main__":
    main()
