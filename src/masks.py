# masks.py

import logging

# 1. Создаем отдельный логер для модуля masks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Уровень логирования — DEBUG и выше

# 2. Настраиваем FileHandler
file_handler = logging.FileHandler('../logs/application.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# 3. Настраиваем форматтер: время, имя модуля, уровень, сообщение
file_formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
)
file_handler.setFormatter(file_formatter)

# 4. Добавляем handler в логер
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты строкой, возвращает замаскированный вариант."""
    logger.debug(f"Вызов get_mask_card_number(card_number={card_number!r})")
    # Убираем все пробелы
    clean = card_number.replace(" ", "")
    # Проверяем валидность
    if len(clean) != 16 or not clean.isdigit():
        logger.error(f"Неверный номер карты: {card_number!r}")
        return "Неверный номер карты"
    # Формируем маску
    part1 = clean[:4]
    part2 = clean[4:6]
    masked = f"{part1} {part2}* *** {clean[-4:]}"
    logger.debug(f"Успешно замаскировано: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Принимает номер счета строкой, возвращает в формате **XXXX."""
    logger.debug(f"Вызов get_mask_account(account_number={account_number!r})")
    clean = account_number.replace(" ", "")
    # Проверяем валидность
    if len(clean) != 20 or not clean.isdigit():
        logger.error(f"Неверный номер счета: {account_number!r}")
        return "Неверный номер счета"
    # Берем последние 4 цифры
    last4 = clean[-4:]
    masked = f"**{last4}"
    logger.debug(f"Успешно замаскировано: {masked}")
    return masked
