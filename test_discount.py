"""Тестирование алгоритма скидки для кинотеатра."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)

    # Список составлен строго по вашей БД фильмов
    test_cases = [
        # (id, цена, ожидание, пояснение)
        (1, 900, 900, "Аватар 2 — есть заказы в сентябре"),
        (2, 800, 800, "Джон Уик 4 — есть заказы в сентябре"),
        (3, 850, 850, "Оппенгеймер — есть заказы в сентябре"),
        (4, 700, 525, "Титаник — нет заказов → 25% скидка"),
        (5, 500, 375, "Шрек — нет заказов → 25% скидка"),
        (6, 750, 562.5, "Оно — нет заказов → 25% скидка"),
        (7, 800, 600, "Гарри Поттер — нет заказов → 25% скидка"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (ФИЛЬМЫ)")
    print("=" * 60)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Фильм {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")
	

if __name__ == "__main__":
    run_tests()
