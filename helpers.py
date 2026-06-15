from datetime import datetime


def read_int(prompt: str) -> int:
    # простой ввод целого числа
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("введите целое число.")


def check_deadline(value: str) -> bool:
    # проверяем формат даты
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def read_deadline(prompt: str = "введите дедлайн в формате гггг-мм-дд: ") -> str:
    # читаем дату, пока не введут нормально
    while True:
        value = input(prompt).strip()
        if check_deadline(value):
            return value
        print("неверный формат даты. пример: 2026-06-15")
