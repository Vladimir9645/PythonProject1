from datetime import datetime

def filter_by_state(dictionary_1, state_value):
    """Фильтрация списка словарей по ключу 'state' и значению state_value"""
    return [d for d in dictionary_1 if d.get('state') == state_value]

def sort_by_date(dictionary_2, date_key="date", date_format="%Y-%m-%dT%H:%M:%S.%f", reverse=False):
    """Сортирует список словарей по дате, учитывая формат даты с временем и миллисекундами"""
    return sorted(
        dictionary_2,
        key=lambda d: datetime.strptime(d[date_key], date_format),
        reverse=reverse
    )

# Исходный список словарей
dictionary = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Использование функции фильтрации
filtered = filter_by_state(dictionary, 'EXECUTED')
print(filtered)
print()

filtered_1 = filter_by_state(dictionary, 'CANCELED')
print(filtered_1)
print()

# Использование функции сортировки
sorted_events = sort_by_date(dictionary, 'date')
print(sorted_events)