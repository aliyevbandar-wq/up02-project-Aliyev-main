"""Модуль централизованной обработки ошибок и валидации данных."""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """
    Безопасный вызов функции с обработкой различных типов исключений (Задание 5.3).
    """
    # ПОПЫТКА:
    try:
        # ВЕРНУТЬ func(*args, **kwargs)
        return func(*args, **kwargs)
        
    # ИСКЛЮЧЕНИЕ FileNotFoundError:
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка файла", f"Критическая ошибка: файл не найден!\n{e}")
        
    # ИСКЛЮЧЕНИЕ ConnectionError:
    except ConnectionError as e:
        messagebox.showerror("Ошибка сети", f"Критическая ошибка: сбой соединения с базой данных!\n{e}")
        
    # ИСКЛЮЧЕНИЕ ValueError:
    except ValueError as e:
        messagebox.showwarning("Неверное значение", f"Предупреждение: некорректные данные!\n{e}")
        
    # ИСКЛЮЧЕНИЕ Exception:
    except Exception as e:
        messagebox.showerror("Непредвиденная ошибка", f"Произошел системный сбой:\n{e}")
        
    # ВЕРНУТЬ None при ошибке
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что значение — положительное целое число (Задание 5.4).
    """
    # ПОПЫТКА:
    try:
        # Попробовать преобразовать value в int
        number = int(value)
        
        # Если получилось и число ≤ 0 -> вернуть (False, f"{field_name} должно быть больше нуля")
        if number <= 0:
            return (False, f"Поле '{field_name}' должно быть больше нуля")
            
        # Если получилось и число > 0 -> вернуть (True, число)
        return (True, number)
        
    # ИСКЛЮЧЕНИЕ ValueError:
    except (ValueError, TypeError):
        # Если не число -> вернуть (False, f"{field_name} должно быть целым числом")
        return (False, f"Поле '{field_name}' должно быть целым числом")
