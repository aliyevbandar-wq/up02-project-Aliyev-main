"""Модуль централизованной обработки ошибок и валидации данных."""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """
    Безопасный вызов функции с обработкой различных типов исключений (Задание 5.3).
    """
    try:
        return func(*args, **kwargs)
        
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка файла", f"Критическая ошибка: файл не найден!\n{e}")
        
    except ConnectionError as e:
        messagebox.showerror("Ошибка сети", f"Критическая ошибка: сбой соединения с базой данных!\n{e}")
        
    except ValueError as e:
        messagebox.showwarning("Неверное значение", f"Предупреждение: некорректные данные!\n{e}")
        
    except Exception as e:
        messagebox.showerror("Непредвиденная ошибка", f"Произошел системный сбой:\n{e}")
        
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что значение — положительное целое число (Задание 5.4 / 5.3 из нового модуля).
    :param value: строка для проверки
    :param field_name: название поля (для сообщения)
    :return: (True, число) или (False, сообщение)
    """
    try:
        number = int(value)
    except (ValueError, TypeError):
        # Строго по шаблону задания
        return (False, f"{field_name} должно быть целым числом")

    if number <= 0:
        # Строго по шаблону задания
        return (False, f"{field_name} должно быть больше нуля")

    return (True, number)
