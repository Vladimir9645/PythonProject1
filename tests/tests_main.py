from unittest.mock import patch, call

import pytest

import main


@pytest.fixture
def sample_transactions():
    """Тестовые данные транзакций."""
    return [
        {
            "state": "EXECUTED",
            "date": "2019-08-12T12:34:56",
            "amount": 40542,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "to": "4321",
            "description": "Открытие вклада"
        },
        {
            "state": "CANCELED",
            "date": "2019-11-12T09:15:22",
            "amount": 130,
            "currency_name": "USD",
            "currency_code": "USD",
            "from": "777127****3727",
            "to": "129338****9203",
            "description": "Перевод с карты на карту"
        },
        {
            "state": "PENDING",
            "date": "2020-01-01T00:00:00",
            "amount": 1000,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "to": "5555",
            "description": "Оплата интернета"
        }
    ]



@patch('builtins.input', side_effect=['1', 'EXECUTED', 'Нет', 'Нет', 'Нет'])
@patch('builtins.print')
@patch('src.financial_transactions_CSV.read_transactions_from_csv')
@patch('src.financial_transactions_Excel.read_transactions_from_excel')
@patch('src.utils.dictionary_with_transaction_data', return_value=sample_transactions())
def test_main_json_executed_no_filters(
    mock_print
):
    """Тест: JSON, статус EXECUTED, без доп. Фильтров."""
    main.main()

    # Проверяем ключевые выводы
    expected_calls = [
        call("Выберите необходимый пункт меню:"),
        call("1. Получить информацию о транзакциях из JSON-файла"),
        call("Введите статус, по которому необходимо выполнить фильтрацию."),
        call("Операции отфильтрованы по статусу EXECUTED"),
        call("Отсортировать операции по дате? Да/Нет"),
        call("Выводить только рублевые транзакции? Да/Нет"),
        call("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"),
        call("Распечатываю итоговый список транзакций..."),
        call("Всего банковских операций в выборке: 1")
    ]
    for exp in expected_calls:
        assert exp in mock_print.call_args_list




@patch('builtins.input', side_effect=['2', 'EXECUTED', 'Да', 'по убыванию', 'Да', 'Нет'])
@patch('builtins.print')
@patch('src.utils.dictionary_with_transaction_data')
@patch('src.financial_transactions_Excel.read_transactions_from_excel')
@patch('src.financial_transactions_CSV.read_transactions_from_csv', return_value=sample_transactions())
@patch('src.processing.sort_by_date')
@patch('src.generators.filter_by_currency')
def test_main_csv_sort_desc_rub(
    mock_print, mock_sort, mock_filter
, sample_transactions):
    """Тест: CSV, EXECUTED, сортировка по убыванию, RUB."""
    main.main()

    mock_sort.assert_called_with(sample_transactions, reverse=True)
    mock_filter.assert_called_with(sample_transactions, "RUB")


    assert call("Операции отфильтрованы по статусу EXECUTED") in mock_print.call_args_list
    assert call("Всего банковских операций в выборке: 1") in mock_print.call_args_list




@patch('builtins.input', side_effect=['3', 'PENDING', 'Нет', 'Нет', 'Да', 'интернет'])
@patch('builtins.print')
@patch('src.utils.dictionary_with_transaction_data')
@patch('src.financial_transactions_CSV.read_transactions_from_csv')
@patch('src.financial_transactions_Excel.read_transactions_from_excel', return_value=sample_transactions())
@patch('src.utils.process_bank_search')
def test_main_excel_search_word(
    mock_print, mock_search
, sample_transactions):
    """Тест: XLSX, PENDING, поиск по слову 'интернет'."""
    mock_search.return_value = [sample_transactions[2]]  # "Оплата интернета"

    main.main()

    mock_search.assert_called_with(sample_transactions, "интернет")
    assert call("Оплата интернета") in mock_print.call_args_list




@patch('builtins.input', side_effect=['1', 'INVALID_STATUS', 'EXECUTED', 'Нет', 'Нет', 'Нет'])
@patch('builtins.print')
@patch('src.utils.dictionary_with_transaction_data', return_value=sample_transactions())
def test_main_invalid_status_retry(mock_print):
    """Тест: неверный статус → повторный запрос."""
    main.main()

    assert call("Статус операции 'INVALID_STATUS' недоступен.") in mock_print.call_args_list
    assert call("Операции отфильтрованы по статусу EXECUTED") in mock_print.call_args_list




@patch('builtins.input', side_effect=['4', '1', 'EXECUTED', 'Нет', 'Нет', 'Нет'])  # 4 — неверный пункт
@patch('builtins.print')
@patch('src.utils.dictionary_with_transaction_data', return_value=sample_transactions())
def test_main_invalid_menu_choice(mock_print):
    """Тест: неверный пункт меню → повторный запрос."""
    main.main()

    menu_calls = [
        call("Выберите необходимый пункт меню:"),
        call("1. Получить информацию о транзакциях из JSON-файла")
    ]
    for mc in menu_calls:
        assert mc in mock_print.call_args_list[:2]  # первые 2 вызова




@patch('builtins.input', side_effect=['1', 'EXECUTED', 'Да', 'по возрастанию', 'Нет', 'Нет'])
@patch('builtins.print')
@patch('src.utils.dictionary_with_transaction_data', return_value=sample_transactions())
@patch('src.processing.sort_by_date')
def test_main_sort_ascending(mock_sort, sample_transactions):
    """Тест: сортировка по возрастанию."""
    main.main()
    mock_sort.assert_called_with(sample_transactions, reverse=False)




@patch('builtins.input', side_effect=['1', 'EXECUTED', 'Нет', 'Да', 'Нет'])
@patch('builtins.print')
@patch('src.utils.dictionary_with_transaction_data', return_value=sample_transactions())
@patch('src.generators.filter_by_currency')
def test_main_filter_rub_only(mock_print, mock_filter, sample_transactions):
    """Тест: фильтрация только RUB."""
    main.main()
    mock_filter.assert_called_with(sample_transactions, "RUB")
    assert call("Всего банковских операций в выборке: 2") in mock_print.call_args_list  # 2 RUB-транзакции




@patch('builtins.input', side_effect=['1', 'EXECUTED', 'Да', 'по убыванию', ''