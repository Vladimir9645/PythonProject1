from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number():
    # Правельный номер карты 16 цифр, без пробелов
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    # Правельный номер с пробелами
    assert get_mask_card_number("1234 56 7890 123456") == "1234 56** **** 3456"

    # Номер слишком короткий
    assert get_mask_card_number("123456789012") == "Неверный номер карты"

    # Номер с символами
    assert (
        get_mask_card_number("1234 56ab 9012 3456") == "Неверный номер карты"
    )

    # Номер слишком длинный
    assert (
        get_mask_card_number("12345678901234567890") == "Неверный номер карты"
    )

    # Пустая строка
    assert get_mask_card_number("") == "Неверный номер карты"


def test_get_mask_account():
    # Правельный номер счета 20 цифр, без пробелов
    assert get_mask_account("12345678901234567890") == "**7890"

    # Правельный номер с пробелами
    assert get_mask_account("1234 5678 9012 3456 7890") == "**7890"

    # Номер счета меньше 20 символов
    assert get_mask_account("1234567890") == "Неверный номер счета"

    # Номер счета больше 20 симфолов
    assert (
        get_mask_account("123456789012345678901234") == "Неверный номер счета"
    )

    # Пустая строка
    assert get_mask_account("") == "Неверный номер счета"
