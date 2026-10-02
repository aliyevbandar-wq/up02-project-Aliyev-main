from datetime import datetime, timedelta

def calculate_price_with_discount(price: float, stock: int) -> float:
    """
    Задание 1: Рассчитывает цену со скидкой 10%, если остаток товара <= 15.
    """
    if stock <= 3:
        return price * 0.90  # Скидка 10%
    return price

def get_previous_month_range(current_date: datetime):
    """
    Шпаргалка: Вычисление начала и конца предыдущего месяца.
    """
    first_day = current_date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    
    return first_day_prev.strftime("%Y-%m-%d"), last_day_prev.strftime("%Y-%m-%d")

# =====================================================================
# Задание 2: 5 тестовых сценариев
# =====================================================================
def run_tests():
    test_cases = [
        # (Цена, Остаток, Ожидаемая цена, Описание)
        (100.0, 2, 90.0,  "Тест 1: Остаток <= 3 (скидка применилась)"),
        (100.0, 3, 90.0,  "Тест 2: Граничное значение 3 (скидка применилась)"),
        (100.0, 4, 100.0, "Тест 3: Остаток > 3 (скидка НЕ применилась)"),
        (500.0, 1, 450.0, "Тест 4: Дорогой товар, мелкий остаток"),
        (0.0,   0, 0.0,   "Тест 5: Нулевая цена и нулевой остаток")
    ]
    
    print("--- Запуск тестов функции скидки ---")
    for i, (price, stock, expected, desc) in enumerate(test_cases, 1):
        result = calculate_price_with_discount(price, stock)
        assert abs(result - expected) < 1e-9, f"Ошибка в {desc}: ожидалось {expected}, получили {result}"
        print(f"[OK] {desc} — Результат: {result}")
    # Проверка
    print("\n--- Проверка дат из шпаргалки ---")
    test_date = datetime(2026, 10, 15)
    start, end = get_previous_month_range(test_date)
    print(f"Для даты {test_date.strftime('%Y-%m-%d')}:")
    print(f"Начало прошлого месяца: {start}")
    print(f"Конец прошлого месяца: {end}")
    
if __name__ == "__main__":
    run_tests()
