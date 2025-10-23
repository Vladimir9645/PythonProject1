def get_mask_card_number(card_number: str) -> str:
    """Функция входа номер карты в виде числа и возврата в виде маски"""
    # Убираем все пробелы из переданной строки
    card_number = card_number.replace(" ", "")
    # Проверяем, что длина карты 16 символов и все символы цифры
    if len(card_number) != 16 or not card_number.isdigit():
        return "Неверный номер карты"
    # Формируем формат XXXX XX** **** XXXX
    # Первые 4 цифры остаются
    part1 = card_number[:4]
    # Следующие 2 цифры остаются
    part2 = card_number[4:6]
    # Далее 2 звёздочки вместо двух цифр
    part2_mask = "**"
    # Потом 4 звёздочки вместо четырех цифр
    part3_mask = "****"
    # Последние 4 цифры остаются
    part4 = card_number[-4:]

    return f"{part1} {part2}{part2_mask} {part3_mask} {part4}"


def get_mask_account(mask_account: str) -> str:
    """функция ввода номера счета и вывода с маской"""

    mask_account = mask_account.replace(" ", "")

    if len(mask_account) != 20 or not mask_account.isdigit():
        return "Неверный номер счета"
    # остаються от 2 до 6
    part_1 = mask_account[16:20]
    # начиная с 2х **
    part_1_mask = "**"
    return f"{part_1_mask}{part_1}"
