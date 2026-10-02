"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    test_cases = [
        # (product_id, price, date, expected, comment)
        # Базовые тесты
        (1, 8500, datetime(2026, 10, 15), 8500, "Заказы есть в сентябре"),
        (2, 15000, datetime(2026, 10, 15), 11250, "Заказов нет → скидка"),
        (3, 12000, datetime(2026, 10, 15), 12000, "Заказы есть"),
        (4, 4500, datetime(2026, 10, 15), 3375, "Заказов нет → скидка"),
        (5, 6000, datetime(2026, 10, 15), 4500, "Заказов нет → скидка"),

        # Новые тесты (из задания)
        (2, 15000, datetime(2026, 11, 15), 15000, "В октябре заказы были?"),
        (1, 8500, datetime(2026, 11, 15), 8500, "В октябре заказы были?"),
        (4, 4500, datetime(2026, 9, 1), 3375, "Август — заказов нет"),

        # Дополнительные тесты (граничные случаи + данные из БД)
        (1, 0, datetime(2026, 10, 15), 0, "Нулевая цена — расчёт без ошибок"),
        (5, 5000, datetime(2026, 10, 15), 3750, "Товар 5 (Шрек) — в сентябре нет заказов → скидка 25%"),
        (2, 8000, datetime(2027, 1, 1), 6000, "1 января — смена года, декабрь без заказов на товар 2 → скидка"),
        (3, 12000, datetime(2026, 10, 31), 12000, "Последний день октября — заказы в сентябре есть → без скидки"),
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

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()
