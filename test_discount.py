<<<<<<< HEAD
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
=======
"""Скрипт проверки алгоритма расчёта скидки на реальной БД."""
from datetime import datetime
import sqlite3
from discount import calculate_price_with_discount, DB_PATH

def run_demonstration_tests():
    # Дата расчета — октябрь 2026 года (так как заказы в БД сделаны в сентябре 2026)
    calculation_date = datetime(2026, 10, 15)
    
    # Подключаемся к вашей реальной БД, чтобы забрать актуальные товары
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, название, цена FROM Товар")
        db_items = cur.fetchall()
        conn.close()
    except sqlite3.OperationalError:
        print(f"❌ Ошибка: Не удалось найти файл базы данных '{DB_PATH}' в текущей папке.")
        return

    # Вывод заголовка
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 60)

    passed_count = 0
    total_count = 0

    # Пробегаем по всем товарам из вашей базы данных
    for item_id, name, base_price in db_items:
        total_count += 1
        
        # Считаем цену со скидкой через функцию из discount.py
        actual_price = calculate_price_with_discount(item_id, base_price, calculation_date)
        
        # Проверяем, были ли заказы, чтобы составить правильное описание для вывода
        # (Используем ту же логику для определения ожидаемого значения)
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Заказ WHERE товар_id = ? AND дата BETWEEN '2026-09-01' AND '2026-09-30'", (item_id,))
        has_orders = cur.fetchone()[0] > 0
        conn.close()

        if has_orders:
            expected_price = base_price
            desc = "есть заказы в сентябре" if item_id == 1 else "есть заказы"
        else:
            expected_price = base_price * 0.75
            desc = "нет заказов → 25% скидка" if item_id == 2 else "нет заказов → скидка"

        # Форматируем вывод чисел (убираем .0 у целых чисел)
        if isinstance(actual_price, float) and actual_price.is_integer():
            actual_price = int(actual_price)
        if isinstance(expected_price, float) and expected_price.is_integer():
            expected_price = int(expected_price)

        # Проверка на совпадение
        if actual_price == expected_price:
            status_emoji = "✅"
            passed_count += 1
        else:
            status_emoji = "❌"

        # Печатаем строку по шаблону
        print(f"{status_emoji} Товар {item_id}: {base_price} → {actual_price} "
              f"(ожидалось {expected_price}) — {name} — {desc}")

    # Вывод подвала программы
    print("=" * 60)
    print(f"Пройдено: {passed_count} / {total_count}")

if __name__ == "__main__":
    run_demonstration_tests()
>>>>>>> dcf49ad74c61951ad79fe1974c51553bc1cedd54
