"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def print_test_report(passed, total):
    """Выводит отчёт о тестировании."""
    print("=" * 40)
    print("ОТЧЁТ О ТЕСТИРОВАНИИ")
    print(f"Пройдено: {passed} / {total}")
    if passed == total:
        print("Результат: ✅ УСПЕХ")
    else:
        print("Результат: ❌ ЕСТЬ ОШИБКИ")
    print("=" * 40)


def run_tests():
    test_cases = [
        # --- Базовые тесты ---
        (1, 8500, datetime(2026, 10, 15), 8500, "Заказы есть в сентябре"),
        (2, 15000, datetime(2026, 10, 15), 11250, "Заказов нет → скидка"),
        (3, 12000, datetime(2026, 10, 15), 12000, "Заказы есть"),
        (4, 4500, datetime(2026, 10, 15), 3375, "Заказов нет → скидка"),
        (5, 6000, datetime(2026, 10, 15), 4500, "Заказов нет → скидка"),

        # --- Новые тесты (из задания 4) ---
        (2, 15000, datetime(2026, 11, 15), 15000, "В октябре заказы были?"),
        (1, 8500, datetime(2026, 11, 15), 8500, "В октябре заказы были?"),
        (4, 4500, datetime(2026, 9, 1), 3375, "Август — заказов нет"),

        # --- 5 новых граничных тестов ---
        # 1. Дата расчёта — 1-е число месяца
        (5, 6000, datetime(2026, 10, 1), 4500, "1-е число месяца — корректный расчёт"),

        # 2. Дата расчёта — последний день месяца
        (5, 6000, datetime(2026, 10, 31), 4500, "Последний день месяца — корректный расчёт"),

        # 3. Товар с нулевой ценой
        (3, 0, datetime(2026, 10, 15), 0, "Нулевая цена — без ошибок"),

        # 4. Товар с отрицательным количеством (проверка валидации)
        (1, -1000, datetime(2026, 10, 15), -1, "Отрицательная цена — отклонено"),

        # 5. Заказы были в позапрошлом месяце, но не в предыдущем
        (2, 15000, datetime(2026, 11, 15), 11250, "Заказы в августе, но не в октябре → скидка"),
    ]

    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print()
    print_test_report(passed, len(test_cases))


if __name__ == "__main__":
    run_tests()
